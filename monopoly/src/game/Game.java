package game;

import Jogadores.Jogador;
import estrategias.AluguelFixo;
import estrategias.AluguelVariavel;
import logradouros.Logradouro;
import logradouros.TipoLogradouro;
import logradouros.regras_especiais.ReceberDinheiro;
import logradouros.regras_especiais.TejePreso;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Game {
    private static Game instance;
    private List<Jogador> jogadores;
    private Tabuleiro tabuleiro;
    private Dado dado;
    private int indexJogadorAtual;
    private LogradouroFactory logradouroFactory;
    private Scanner scanner;

    private Game() {
        this.jogadores = new ArrayList<>();
        this.logradouroFactory = new LogradouroFactory();
        this.tabuleiro = criarTabuleiro(logradouroFactory);
        this.dado = new Dado();
        this.indexJogadorAtual = 0;
        this.scanner = new Scanner(System.in);
    }

    public static Game getInstance() {
        if (instance == null) {
            instance = new Game();
        }
        return instance;
    }

    public void addJogador(Jogador jogador) {
        this.jogadores.add(jogador);
    }

    public void startGame() {
        if (jogadores.size() < 2) {
            System.out.println("É necessário pelo menos 2 jogadores para iniciar o jogo.");
            return;
        }
        System.out.println("O jogo Monopoly Textual Iniciou!");
        while (!isGameOver()) {
            jogarRodada();
        }
        Jogador winner = getGanhador();
        if (winner != null) {
            System.out.println("Parabéns, " + winner.getNome() + "! Você venceu o jogo!");
        } else {
            System.out.println("O jogo terminou sem vencedor.");
        }
    }

    public void jogarRodada() {
        Jogador jogadorAtual = getJogadorAtual();
        System.out.println("\nTurno de " + jogadorAtual.getNome() + "!");
        System.out.println("Saldo atual: $" + String.format("%.2f", jogadorAtual.getSaldo()));
        jogadorAtual.displayPortfolio();

        System.out.print("Pressione ENTER para lançar os dados...");
        scanner.nextLine();

        int diceValue = rolarDados();
        System.out.println(jogadorAtual.getNome() + " lançou " + diceValue + " nos dados.");

        moverJogador(jogadorAtual, diceValue);
        Logradouro currentSpace = tabuleiro.getLogradouro(jogadorAtual.getPosicao());
        System.out.println(jogadorAtual.getNome() + " caiu em " + currentSpace.getNome() + ".");

        currentSpace.novaPosicao(jogadorAtual, this);

        proximoJogador();
        checkSaldoNegativo();
    }

    private void moverJogador(Jogador jogador, int valorDado) {
        int posicaoAtual = jogador.getPosicao();
        int novaPosicao = (posicaoAtual + valorDado) % tabuleiro.getLogradouroCount();
        jogador.setPosicao(novaPosicao);
        if (novaPosicao < posicaoAtual) {
            jogador.receberDinheiro(100); // Passou pelo ponto de partida, recebe $100
            System.out.println(getJogadorAtual().getNome() + " passou pelo Ponto de Partida e recebeu $100.");
        }
    }

    public Jogador getJogadorAtual() {
        return jogadores.get(indexJogadorAtual);
    }

    public Tabuleiro getTabuleiro() {
        return tabuleiro;
    }

    public int rolarDados() {
        return dado.roll();
    }

    public void proximoJogador() {
        indexJogadorAtual = (indexJogadorAtual + 1) % jogadores.size();
    }

    public boolean isGameOver() {
        int activePlayers = 0;
        for (Jogador jogador : jogadores) {
            if (jogador.getSaldo() >= 0) { // Jogador com saldo negativo está eliminado
                activePlayers++;
            }
        }
        return activePlayers <= 1;
    }

    public Jogador getGanhador() {
        if (!isGameOver()) {
            return null;
        }
        for (Jogador jogador : jogadores) {
            if (jogador.getSaldo() >= 0) {
                return jogador;
            }
        }
        return null;
    }

    private Tabuleiro criarTabuleiro(LogradouroFactory factory) {
        Tabuleiro tabuleiro1 = new Tabuleiro(factory);
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.IMOVEL, "Avenida Principal", 200.0, 50.0));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.EMPRESA, "Companhia de Energia", 150.0, new AluguelFixo(30.0)));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.ESPECIAL, "Sorte ou Revés", new ReceberDinheiro(50.0)));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.IMOVEL, "Rua da Praia", 180.0, 40.0));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.EMPRESA, "Companhia de Água", 150.0, new AluguelVariavel(10.0)));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.ESPECIAL, "Visita à Prisão", new TejePreso()));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.IMOVEL, "Avenida Central", 220.0, 60.0));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.EMPRESA, "Companhia de Gás", 150.0, new AluguelFixo(35.0)));
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.ESPECIAL, "Ponto de Partida")); // Ponto de partida - posição 0
        tabuleiro1.addLogradouro(factory.criaLogradouro(TipoLogradouro.IMOVEL, "Rua das Flores", 160.0, 35.0));
        return tabuleiro1;
    }

    private void checkSaldoNegativo() {
        List<Jogador> jogadoresFalidos = new ArrayList<>();
        for (Jogador jogador : jogadores) {
            if (jogador.getSaldo() < 0) {
                jogadoresFalidos.add(jogador);
            }
        }

        for (Jogador jogadorFalido : jogadoresFalidos) {
            System.out.println("\nJogador " + jogadorFalido.getNome() + " faliu e está fora do jogo!");
            jogadores.remove(jogadorFalido);
            if (jogadores.size() == 1) return;
            if (indexJogadorAtual >= jogadores.size()) {
                indexJogadorAtual = 0;
            }
        }
    }

    public Scanner getScanner() {
        return this.scanner;
    }
}
