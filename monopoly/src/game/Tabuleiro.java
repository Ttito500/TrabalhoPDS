package game;

import logradouros.Logradouro;

import java.util.ArrayList;
import java.util.List;

public class Tabuleiro {
    private List<Logradouro> logradouros;

    public Tabuleiro(LogradouroFactory logradouroFactory) {
        this.logradouros = new ArrayList<>();
    }

    public void addLogradouro(Logradouro logradouro) {
        this.logradouros.add(logradouro);
    }

    public Logradouro getLogradouro(int position) {
        if (position < 0 || position >= logradouros.size()) {
            return logradouros.get(0); // Ponto de partida se posição inválida
        }
        return logradouros.get(position);
    }

    public int getLogradouroCount() {
        return logradouros.size();
    }
}
