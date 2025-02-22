import Jogadores.Jogador;
import game.Game;

public class Main {
    public static void main(String[] args) {
        Game game = Game.getInstance();

        Jogador player1 = new Jogador("Jogador 1", 1500.0);
        Jogador player2 = new Jogador("Jogador 2", 1500.0);

        game.addJogador(player1);
        game.addJogador(player2);

        game.startGame();
    }
}
