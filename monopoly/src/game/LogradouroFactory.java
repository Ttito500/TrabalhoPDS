package game;

import estrategias.AluguelStrategy;
import logradouros.*;
import logradouros.regras_especiais.RegraEspecial;

public class LogradouroFactory {
    public Logradouro criaLogradouro(TipoLogradouro tipo, String nome, Object... args) {
        switch (tipo) {
            case IMOVEL:
                return new Imovel(nome, (Double) args[0], (Double) args[1]);
            case EMPRESA:
                return new Empresa(nome, (Double) args[0], (AluguelStrategy) args[1]);
            case ESPECIAL:
                RegraEspecial regraEspecial = (args != null && args.length > 0 && args[0] instanceof RegraEspecial) ? (RegraEspecial) args[0] : null;
                return new LugarEspecial(nome, regraEspecial);
            default:
                return new LugarEspecial(nome, null); // Lugar especial padrão se tipo desconhecido
        }
    }
}