package logradouros.regras_especiais;

import Jogadores.Jogador;
import game.Game;

public class ReceberDinheiro implements RegraEspecial{
    private double quatia;

    public ReceberDinheiro(double quatia) {
        this.quatia = quatia;
    }

    @Override
    public void executar(Jogador player, Game game) {
        player.receberDinheiro(quatia);
        System.out.println(player.getNome() + " recebeu $" + quatia + " de Sorte ou Revés.");
    }
}
