package logradouros.regras_especiais;

import Jogadores.Jogador;
import game.Game;

public class TejePreso implements RegraEspecial{
    @Override
    public void executar(Jogador player, Game game) {
        System.out.println(player.getNome() + " foi para a Visita à Prisão! (Nada acontece).");
    }
}
