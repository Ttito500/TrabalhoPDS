package logradouros;

import Jogadores.Jogador;
import estrategias.AluguelStrategy;
import game.Game;

import java.util.Scanner;

public class Empresa extends Logradouro{
    private double valorCompra;
    private AluguelStrategy aluguelStrategy;
    private Jogador dono;

    public Empresa(String name, double valorCompra, AluguelStrategy aluguelStrategy) {
        super(name);
        this.valorCompra = valorCompra;
        this.aluguelStrategy = aluguelStrategy;
        this.dono = null;
    }

    public double getValorCompra() {
        return valorCompra;
    }

    public double getValorAluguel(int valorDado) {
        return aluguelStrategy.calcularAluguel(valorDado);
    }

    public Jogador getDono() {
        return dono;
    }

    public void setDono(Jogador dono) {
        this.dono = dono;
    }

    public void setAluguelStrategy(AluguelStrategy aluguelStrategy) {
        this.aluguelStrategy = aluguelStrategy;
    }

    public boolean isOwned() {
        return dono != null;
    }

    @Override
    public void novaPosicao(Jogador player, Game game) {
        super.novaPosicao(player, game);
        if (isOwned()) {
            if (dono != player) {
                pagarTaxaUso(player, game);
            } else {
                System.out.println(player.getNome() + " já possui esta empresa.");
            }
        } else {
            oferecerCompra(player, game);
        }
    }

    private void pagarTaxaUso(Jogador jogador, Game game) {
        int diceValue = game.rolarDados(); // Empresa variável usa valor dos dados
        double taxaUso = getValorAluguel(diceValue);
        boolean paymentSuccessful = jogador.pagarDinheiro(taxaUso);
        if (paymentSuccessful) {
            dono.receberDinheiro(taxaUso);
            System.out.println(jogador.getNome() + " pagou $" + taxaUso + " de taxa de uso para " + dono.getNome() + ".");
        } else {
            System.out.println(jogador.getNome() + " não conseguiu pagar a taxa de uso e está falido!");
        }
    }

    private void oferecerCompra(Jogador jogador, Game game) {
        Scanner scanner = game.getScanner();
        System.out.print("Deseja comprar " + getNome() + " por $" + getValorCompra() + "? (sim/não): ");
        String answer = scanner.nextLine();
        if (answer.equalsIgnoreCase("sim")) {
            if (jogador.getSaldo() >= valorCompra) {
                jogador.pagarDinheiro(valorCompra);
                setDono(jogador);
                jogador.addEmpresa(this);
                System.out.println(jogador.getNome() + " comprou " + getNome() + "!");
            } else {
                System.out.println(jogador.getNome() + " não tem saldo suficiente para comprar " + getNome() + ".");
            }
        }
    }
}
