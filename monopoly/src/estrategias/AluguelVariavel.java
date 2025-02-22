package estrategias;

public class AluguelVariavel implements AluguelStrategy{
    private double multiplicadorAluguel;

    public AluguelVariavel(double multiplicadorAluguel){
        this.multiplicadorAluguel = multiplicadorAluguel;
    }

    @Override
    public double calcularAluguel(int valorDado) {
        return valorDado * multiplicadorAluguel;
    }
}
