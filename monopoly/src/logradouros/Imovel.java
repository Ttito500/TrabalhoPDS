package logradouros;

import Jogadores.Jogador;
import game.Game;

import java.util.Scanner;

public class Imovel extends Logradouro{
    private double valorCompra;
    private double valorAluguel;
    private Jogador dono;

    public Imovel(String nome, double valorCompra, double valorAluguel) {
        super(nome);
        this.valorCompra = valorCompra;
        this.valorAluguel = valorAluguel;
        this.dono = null;
    }

    public double getValorCompra() {
        return valorCompra;
    }

    public double getValorAluguel() {
        return valorAluguel;
    }

    public Jogador getDono() {
        return dono;
    }

    public void setDono(Jogador dono) {
        this.dono = dono;
    }

    public boolean isOwned() {
        return dono != null;
    }

    @Override
    public void novaPosicao(Jogador jogador, Game game) {
        super.novaPosicao(jogador, game);
        if (isOwned()) {
            if (dono != jogador) {
                pagarAluguel(jogador, game);
            } else {
                System.out.println(jogador.getNome() + " já possui este imóvel.");
            }
        } else {
            oferecerCompra(jogador, game);
        }
    }

    private void pagarAluguel(Jogador jogador, Game game) {
        double rent = getValorAluguel();
        boolean paymentSuccessful = jogador.pagarDinheiro(rent);
        if (paymentSuccessful) {
            dono.receberDinheiro(rent);
            System.out.println(jogador.getNome() + " pagou $" + rent + " de aluguel para " + dono.getNome() + ".");
        } else {
            System.out.println(jogador.getNome() + " não conseguiu pagar o aluguel e está falido!");
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
                jogador.addImovel(this);
                System.out.println(jogador.getNome() + " comprou " + getNome() + "!");
            } else {
                System.out.println(jogador.getNome() + " não tem saldo suficiente para comprar " + getNome() + ".");
            }
        }
    }
}
