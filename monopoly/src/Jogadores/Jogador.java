package Jogadores;

import game.Tabuleiro;
import logradouros.Empresa;
import logradouros.Imovel;

import java.util.List;

public class Jogador {
    private String nome;
    private Portifolio portifolio;
    private int posicao;

    public Jogador(String name, double dinheiroInicial) {
        this.nome = name;
        this.portifolio = new Portifolio(dinheiroInicial);
        this.posicao = 0; // Inicia no Ponto de Partida
    }

    public String getNome() {
        return nome;
    }

    public double getSaldo() {
        return portifolio.getSaldo();
    }

    public List<Imovel> getProperties() {
        return portifolio.getImoveis();
    }

    public List<Empresa> getCompanies() {
        return portifolio.getEmpresas();
    }

    public int getPosicao() {
        return posicao;
    }

    public void setPosicao(int posicao) {
        this.posicao = posicao;
    }

    public void receberDinheiro(double quantia) {
        portifolio.depositar(quantia);
    }

    public boolean pagarDinheiro(double quantia) {
        return portifolio.sacar(quantia);
    }

    public void addImovel(Imovel imovel) {
        portifolio.addImovel(imovel);
    }

    public void addEmpresa(Empresa empresa) {
        portifolio.addEmpresa(empresa);
    }

    public void displayPortfolio() {
        System.out.println("\n--- Portfólio de " + getNome() + " ---");
        portifolio.display();
    }

    public void move(int valorDado, Tabuleiro tabuleiro) {
        int oldPosition = posicao;
        posicao = (posicao + valorDado) % tabuleiro.getLogradouroCount();
        if (posicao < oldPosition) {
            receberDinheiro(100); // Passou pelo ponto de partida
            System.out.println(getNome() + " passou pelo Ponto de Partida e recebeu $100.");
        }
    }
}
