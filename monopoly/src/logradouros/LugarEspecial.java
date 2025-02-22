package logradouros;

import Jogadores.Jogador;
import game.Game;
import logradouros.regras_especiais.RegraEspecial;

public class LugarEspecial extends Logradouro{
    private RegraEspecial regra;

    public LugarEspecial(String nome, RegraEspecial regra) {
        super(nome);
        this.regra = regra;
    }

    public void novaPosicao(Jogador jogador, Game game) {
        super.novaPosicao(jogador, game);
        if (regra != null) {
            regra.executar(jogador, game);
        } else {
            System.out.println("Lugar especial sem ação definida.");
        }
    }
}
