package logradouros;

import Jogadores.Jogador;
import game.Game;

public abstract class Logradouro {
    private String nome;

    public Logradouro(String name) {
        this.nome = name;
    }

    public String getNome() {
        return nome;
    }

    public void novaPosicao(Jogador player, Game game) {
        System.out.println(player.getNome() + " está no logradouro " + getNome() + ".");
    }

    @Override
    public String toString() {
        return nome;
    }
}
