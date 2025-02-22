package logradouros.regras_especiais;

import Jogadores.Jogador;
import game.Game;

public interface RegraEspecial {
    void executar(Jogador player, Game game);
}
