package estrategias;

public class AluguelFixo implements AluguelStrategy{
    private double valorAluguel;

    public AluguelFixo(double valorAluguel){
        this.valorAluguel = valorAluguel;
    }

    @Override
    public double calcularAluguel(int valorDado) {
        return valorAluguel;
    }
}
