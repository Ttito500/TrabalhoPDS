import random
import math
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from abc import ABC, abstractmethod

# ====================================
# Padrão Observer
# ====================================

class Observer(ABC):
    @abstractmethod
    def update(self, event: str):
        pass

# ====================================
# Modelo – Lógica do Jogo
# ====================================

# Classe base para os logradouros (polimorfismo)
class Space(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def landed_on(self, player, dice_values, game):
        pass

# Imóvel: pode ser adquirido e rende aluguel
class Property(Space):
    def __init__(self, name: str, price: int, rent: int):
        super().__init__(name)
        self.price = price
        self.rent = rent
        self.owner = None

    def landed_on(self, player, dice_values, game):
        if self.owner is None:
            game.log_event(f"{player.name} caiu em {self.name} (Imóvel). Preço: {self.price}, Aluguel: {self.rent}.")
            game.offer_purchase(player, self)
        elif self.owner != player:
            game.log_event(f"{player.name} caiu em {self.name}, que pertence a {self.owner.name}. Deve pagar aluguel de {self.rent}.")
            if not player.pay(self.rent, self.owner):
                game.eliminate_player(player)
        else:
            game.log_event(f"{player.name} caiu em seu próprio imóvel {self.name}.")

# Empresa: pode ser adquirida e rende taxa de uso (Strategy)
class Company(Space):
    def __init__(self, name: str, price: int, base_fee: int, fee_strategy):
        super().__init__(name)
        self.price = price
        self.base_fee = base_fee
        self.owner = None
        self.fee_strategy = fee_strategy

    def landed_on(self, player, dice_values, game):
        if self.owner is None:
            game.log_event(f"{player.name} caiu na {self.name} (Empresa). Preço: {self.price}, Taxa Base: {self.base_fee}.")
            game.offer_purchase(player, self)
        elif self.owner != player:
            fee = self.fee_strategy.calculate_fee(self, dice_values)
            game.log_event(f"{player.name} caiu na {self.name}, que pertence a {self.owner.name}. Deve pagar taxa de {fee}.")
            if not player.pay(fee, self.owner):
                game.eliminate_player(player)
        else:
            game.log_event(f"{player.name} caiu em sua própria empresa {self.name}.")

# Lugar Especial: não pode ser adquirido e possui efeito especial
class SpecialPlace(Space):
    def __init__(self, name: str, effect):
        super().__init__(name)
        self.effect = effect

    def landed_on(self, player, dice_values, game):
        game.log_event(f"{player.name} caiu em {self.name} (Lugar Especial).")
        self.effect(player, game)

# ====================================
# Padrão Strategy – Cálculo de Taxa
# ====================================

class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, company, dice_values):
        pass

class FixedFeeStrategy(FeeStrategy):
    def calculate_fee(self, company, dice_values):
        return company.base_fee

class VariableFeeStrategy(FeeStrategy):
    def calculate_fee(self, company, dice_values):
        return company.base_fee * sum(dice_values)

# ====================================
# Padrão Factory – Criação dos Espaços
# ====================================

class SpaceFactory:
    @staticmethod
    def create_space(space_type: str, **kwargs):
        if space_type == 'property':
            return Property(kwargs['name'], kwargs['price'], kwargs['rent'])
        elif space_type == 'company':
            fee_strategy_type = kwargs.get('fee_strategy', 'fixed')
            fee_strategy = FixedFeeStrategy() if fee_strategy_type == 'fixed' else VariableFeeStrategy()
            return Company(kwargs['name'], kwargs['price'], kwargs['base_fee'], fee_strategy)
        elif space_type == 'special':
            return SpecialPlace(kwargs['name'], kwargs['effect'])
        else:
            raise ValueError("Tipo de logradouro inválido.")

# ====================================
# Classe Player
# ====================================

class Player:
    def __init__(self, name: str, balance: int = 500):
        self.name = name
        self.balance = balance
        self.properties = []  # Logradouros adquiridos
        self.position = 0

    def add_property(self, space: Space):
        self.properties.append(space)

    def adjust_balance(self, amount: int):
        self.balance += amount

    def pay(self, amount: int, recipient):
        if self.balance >= amount:
            self.balance -= amount
            recipient.adjust_balance(amount)
            return True
        else:
            return False

# ====================================
# Classe Board (Tabuleiro)
# ====================================

class Board:
    def __init__(self, spaces: list):
        self.spaces = spaces
        self.start_position = 0

    def get_space(self, position: int):
        return self.spaces[position % len(self.spaces)]

# ====================================
# Classe Game (Lógica Central)
# ====================================

class Game:
    def __init__(self, board: Board, players: list, starting_bonus: int = 100):
        self.board = board
        self.players = players
        self.current_player_index = 0
        self.starting_bonus = starting_bonus
        self.active = True
        self.observers = []  # Para notificação de eventos
        self.purchase_callback = None

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def log_event(self, event: str):
        for observer in self.observers:
            observer.update(event)
        print(event)

    def offer_purchase(self, player: Player, space: Space):
        if self.purchase_callback:
            decision = self.purchase_callback(player, space)
        else:
            decision = True
        if decision:
            if player.balance >= space.price:
                player.adjust_balance(-space.price)
                space.owner = player
                player.add_property(space)
                self.log_event(f"{player.name} comprou {space.name} por {space.price}.")
            else:
                self.log_event(f"{player.name} não tem saldo suficiente para comprar {space.name}.")
        else:
            self.log_event(f"{player.name} optou por não comprar {space.name}.")

    def eliminate_player(self, player: Player):
        self.log_event(f"{player.name} foi eliminado!")
        if player in self.players:
            self.players.remove(player)
        if len(self.players) == 1:
            self.log_event(f"{self.players[0].name} é o vencedor!")
            self.active = False

# ====================================
# Efeitos para Lugares Especiais
# ====================================

def bonus_effect(player: Player, game: Game):
    bonus = 50
    game.log_event(f"{player.name} recebe um bônus de {bonus}.")
    player.adjust_balance(bonus)

def penalty_effect(player: Player, game: Game):
    penalty = 50
    game.log_event(f"{player.name} sofre uma penalidade de {penalty}.")
    player.adjust_balance(-penalty)
    if player.balance < 0:
         game.eliminate_player(player)

def move_effect(steps: int):
    def effect(player: Player, game: Game):
        game.log_event(f"{player.name} avança {steps} casa(s).")
        player.position += steps
    return effect

# ====================================
# Interface Gráfica (Tkinter) – Visualiza Tabuleiro, Logradouros e Animação dos Dados
# ====================================

class GameUI(Observer):
    def __init__(self, game: Game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Jogo de Tabuleiro")

        # ----- Top: Informação do turno e botões de dados -----
        self.top_frame = tk.Frame(self.root)
        self.top_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")

        # Label de turno (mantido na coluna 0, à esquerda)
        self.turn_label = tk.Label(self.top_frame, text="Aguardando o início do jogo...", font=("Arial", 14, "bold"))
        self.turn_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Botão "Lançar Dados" (agora no top_frame, coluna 1, à direita)
        self.dice_button = tk.Button(self.top_frame, text="Lançar Dados", command=self.roll_dice, font=("Arial", 12))
        self.dice_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Label de resultado dos dados (agora no top_frame, coluna 2, à direita)
        self.dice_result_label = tk.Label(self.top_frame, text="Resultado: ", font=("Arial", 12))
        self.dice_result_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")


        # ----- Middle: 3 Colunas (Portfólios, Tabuleiro e Log) -----
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Coluna 0: Portfólios dos Jogadores
        self.portfolio_frame = tk.Frame(self.middle_frame, bd=2, relief=tk.SUNKEN)
        self.portfolio_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        self.portfolio_labels = {}
        for player in self.game.players:
            frame = tk.LabelFrame(self.portfolio_frame, text=player.name, padx=3, pady=3)
            frame.pack(pady=3, fill=tk.X)
            balance_label = tk.Label(frame, text=f"Saldo: {player.balance}", font=("Arial", 10))
            balance_label.pack(anchor=tk.W)
            position_label = tk.Label(frame, text=f"Posição: {player.position}", font=("Arial", 10))
            position_label.pack(anchor=tk.W)
            properties_label = tk.Label(frame, text="Logradouros: Nenhum", font=("Arial", 10))
            properties_label.pack(anchor=tk.W)
            self.portfolio_labels[player.name] = {
                'balance': balance_label,
                'position': position_label,
                'properties': properties_label,
            }

        # Coluna 1: Visualização do Tabuleiro (Canvas + Lista de Logradouros)
        self.board_frame = tk.Frame(self.middle_frame, bd=2, relief=tk.SUNKEN)
        self.board_frame.grid(row=0, column=1, padx=5, pady=5)
        # Canvas maior e estilizado - DIMINUINDO O CANVAS
        self.board_canvas = tk.Canvas(self.board_frame, width=500, height=500, bg="ivory") # Reduzido width and height from 600 to 500
        self.board_canvas.pack()
        self.spaces_listbox = tk.Listbox(self.board_frame, width=40, font=("Arial", 9)) # Reduzido width from 50 to 40 and font from 10 to 9
        self.spaces_listbox.pack(pady=3, fill=tk.X) # Reduced pady from 5 to 3
        self.update_space_details()

        # Coluna 2: Log de Eventos
        self.log_frame = tk.Frame(self.middle_frame)
        self.log_frame.grid(row=0, column=2, padx=5, pady=5)
        self.log_text = ScrolledText(self.log_frame, state='disabled', width=30, height=25, font=("Arial", 9)) # Reduzido width from 40 to 30, height from 30 to 25, and font from 10 to 9
        self.log_text.pack(padx=5, pady=5) # Reduced padx and pady from 10 to 5


        self.waiting_for_roll = False
        self.current_dice = None

        # ----- Geração de posições quadradas para 30 espaços -----
        self.space_positions = []
        canvas_width = 500 # Ajustar para o novo tamanho do canvas
        canvas_height = 500 # Ajustar para o novo tamanho do canvas
        square_side = 400 # Reduzir o tamanho do quadrado interno para caber no canvas menor
        start_x = (canvas_width - square_side) / 2
        start_y = (canvas_height - square_side) / 2
        num_spaces = len(self.game.board.spaces)
        spaces_per_side = num_spaces // 4
        extra_spaces = num_spaces % 4

        positions = []
        # Lado superior
        for i in range(spaces_per_side + (1 if extra_spaces > 0 else 0)):
            x = start_x + i * (square_side / (spaces_per_side + (1 if extra_spaces > 0 else 0) -1 if (spaces_per_side + (1 if extra_spaces > 0 else 0)) > 1 else 1 ))
            y = start_y
            positions.append((x, y))
        # Lado direito
        for i in range(1, spaces_per_side + (1 if extra_spaces > 1 else 0)): # Start from 1 to avoid repeating corner
            x = start_x + square_side
            y = start_y + i * (square_side / (spaces_per_side + (1 if extra_spaces > 1 else 0) -1 if (spaces_per_side + (1 if extra_spaces > 1 else 0)) > 1 else 1 ))
            positions.append((x, y))
        # Lado inferior
        for i in range(1, spaces_per_side + (1 if extra_spaces > 2 else 0)): # Start from 1 to avoid repeating corner
            x = start_x + square_side - i * (square_side / (spaces_per_side + (1 if extra_spaces > 2 else 0) -1 if (spaces_per_side + (1 if extra_spaces > 2 else 0)) > 1 else 1 ))
            y = start_y + square_side
            positions.append((x, y))
        # Lado esquerdo
        for i in range(1, spaces_per_side + (1 if extra_spaces > 3 else 0) ): # Start from 1 to avoid repeating corner
            x = start_x
            y = start_y + square_side - i * (square_side / (spaces_per_side + (1 if extra_spaces > 3 else 0) -1 if (spaces_per_side + (1 if extra_spaces > 3 else 0)) > 1 else 1 ))
            positions.append((x, y))

        self.space_positions = positions[:num_spaces] # Trim if more positions than spaces


    def update(self, event: str):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, event + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)
        if event.startswith("É a vez de"):
            self.turn_label.config(text=event, font=("Arial", 14, "bold"), fg="black") # Restaura a cor e fonte padrão para o turno
        elif event.startswith("Jogador ") and event.endswith(" é o vencedor!"): # Detecta a mensagem de vitória
            winner_name = event.split(" ")[0] + " " + event.split(" ")[1] # Extrai o nome do vencedor da mensagem
            self.victory_animation(winner_name) # Chama a animação de vitória
        self.update_portfolios()
        self.draw_board()
        self.update_space_details()

    def update_portfolios(self):
        for player in self.game.players:
            labels = self.portfolio_labels.get(player.name)
            if labels:
                labels['balance'].config(text=f"Saldo: {player.balance}")
                labels['position'].config(text=f"Posição: {player.position % len(self.game.board.spaces)}")
                props = ', '.join([prop.name for prop in player.properties]) if player.properties else "Nenhum"
                labels['properties'].config(text=f"Logradouros: {props}")

    def draw_board(self):
        self.board_canvas.delete("all")
        n = len(self.game.board.spaces)
        # Desenha o caminho quadrado conectando os pontos com uma linha estilizada
        if len(self.space_positions) > 1:
            for i in range(len(self.space_positions) - 1):
                x1, y1 = self.space_positions[i]
                x2, y2 = self.space_positions[i+1]
                self.board_canvas.create_line(x1, y1, x2, y2, fill="darkblue", width=3)
            # Fecha o caminho (if needed for square, usually it closes automatically)
            x1, y1 = self.space_positions[-1]
            x2, y2 = self.space_positions[0]
            self.board_canvas.create_line(x1, y1, x2, y2, fill="darkblue", width=3)

        # Desenha cada espaço com círculos maiores e estilo diferenciado
        space_diameter = 50
        for i, pos in enumerate(self.space_positions):
            x, y = pos
            self.board_canvas.create_oval(x - space_diameter/2, y - space_diameter/2,
                                          x + space_diameter/2, y + space_diameter/2,
                                          fill="lightblue", outline="navy", width=2)
            space = self.game.board.spaces[i]
            self.board_canvas.create_text(x, y, text=f"{i}\n{space.name}", font=("Arial", 9, "bold"), fill="navy", justify="center")
        # Desenha os jogadores com marcadores coloridos
        colors = ["red", "blue", "green", "orange", "purple"]
        for idx, player in enumerate(self.game.players):
            pos_index = player.position % n
            x, y = self.space_positions[pos_index]
            marker_radius = 12
            self.board_canvas.create_oval(x - marker_radius, y - marker_radius,
                                          x + marker_radius, y + marker_radius,
                                          fill=colors[idx % len(colors)], outline="black", width=2)
            initials = ''.join([word[0] for word in player.name.split()])
            self.board_canvas.create_text(x, y, text=initials, font=("Arial", 10, "bold"), fill="white")

    def update_space_details(self):
        self.spaces_listbox.delete(0, tk.END)
        for i, space in enumerate(self.game.board.spaces):
            if isinstance(space, Property):
                detail = f"{i}: {space.name} - Imóvel | Preço: {space.price} | Aluguel: {space.rent}"
            elif isinstance(space, Company):
                detail = f"{i}: {space.name} - Empresa | Preço: {space.price} | Taxa Base: {space.base_fee}"
            elif isinstance(space, SpecialPlace):
                detail = f"{i}: {space.name} - Lugar Especial"
            else:
                detail = f"{i}: {space.name} - Desconhecido"
            self.spaces_listbox.insert(tk.END, detail)

    def roll_dice(self):
        # Inicia a animação desabilitando o botão
        self.dice_button.config(state=tk.DISABLED)
        self.animation_iterations = 10  # número de frames da animação
        self.animate_dice()

    def animate_dice(self):
        if self.animation_iterations > 0:
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            self.dice_result_label.config(text=f"Rolando... {d1} e {d2}")
            self.animation_iterations -= 1
            self.root.after(100, self.animate_dice)
        else:
            # Resultado final dos dados
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            self.current_dice = [d1, d2]
            self.dice_result_label.config(text=f"Resultado: {d1} e {d2} (Total: {d1+d2})")
            self.waiting_for_roll = False
            self.dice_button.config(state=tk.NORMAL)

    def ask_purchase(self, player: Player, space: Space):
        return messagebox.askyesno("Opção de Compra", f"{player.name}, deseja comprar {space.name} por {space.price}?")

    def victory_animation(self, winner_name: str):
        messagebox.showinfo("Vitória!", f"{winner_name} é o grande Vencedor!")
        self.turn_label.config(text=f"{winner_name} é o Vencedor!", font=("Arial", 20, "bold"), fg="darkgreen")
        # Você pode adicionar efeitos visuais adicionais aqui, se desejar, como mudar a cor de fundo do tabuleiro, etc.


    def start(self):
        self.root.mainloop()

# ====================================
# Controller do Jogo (Integra Lógica e Interface)
# ====================================

class GameController:
    def __init__(self, game: Game, ui: GameUI):
        self.game = game
        self.ui = ui
        self.game.add_observer(ui)
        self.game.purchase_callback = ui.ask_purchase
        self.current_turn_player = None

    def start_game(self):
        self.game.log_event("Iniciando o jogo.")
        self.process_turn()

    def process_turn(self):
        if not self.game.active or len(self.game.players) == 0:
            return
        player = self.game.players[self.game.current_player_index]
        self.current_turn_player = player
        self.game.log_event(f"É a vez de {player.name}.")
        self.ui.waiting_for_roll = True
        self.check_dice_roll()

    def check_dice_roll(self):
        if self.ui.current_dice is not None:
            dice_values = self.ui.current_dice
            self.ui.current_dice = None
            player = self.current_turn_player
            steps = sum(dice_values)
            self.game.log_event(f"{player.name} rolou os dados: {dice_values} totalizando {steps}.")
            prev_position = player.position
            player.position += steps
            if player.position // len(self.game.board.spaces) > prev_position // len(self.game.board.spaces):
                player.adjust_balance(self.game.starting_bonus)
                self.game.log_event(f"{player.name} passou pelo Ponto de Partida e recebeu {self.game.starting_bonus}.")
            current_space = self.game.board.get_space(player.position)
            current_space.landed_on(player, dice_values, self.game)
            if self.game.active:
                self.game.current_player_index = (self.game.current_player_index + 1) % len(self.game.players)
                self.ui.root.after(1000, self.process_turn)
        else:
            self.ui.root.after(100, self.check_dice_roll)

# ====================================
# Função Principal
# ====================================

def main():
    # Criação de um tabuleiro com 30 espaços usando uma variação entre os tipos
    spaces = []
    for i in range(30):
        if i == 0:
            spaces.append(SpecialPlace("Ponto de Partida", lambda p, g: None))
        else:
            if i % 3 == 0:
                spaces.append(SpaceFactory.create_space('property', name=f"Rua {i}", price=100 + i * 10, rent=10 + i))
            elif i % 3 == 1:
                fee_strategy = 'fixed' if i % 2 == 0 else 'variable'
                spaces.append(SpaceFactory.create_space('company', name=f"Empresa {i}", price=150 + i * 5, base_fee=5 + i, fee_strategy=fee_strategy))
            else:
                if i % 2 == 0:
                    spaces.append(SpaceFactory.create_space('special', name=f"Praça {i}", effect=bonus_effect))
                else:
                    spaces.append(SpaceFactory.create_space('special', name=f"Penalidade {i}", effect=move_effect(1)))

    board = Board(spaces)
    player1 = Player("Jogador 1")
    player2 = Player("Jogador 2")
    players = [player1, player2]
    game = Game(board, players, starting_bonus=100)
    ui = GameUI(game)
    controller = GameController(game, ui)
    ui.root.after(1000, controller.start_game)
    ui.start()

if __name__ == "__main__":
    main()