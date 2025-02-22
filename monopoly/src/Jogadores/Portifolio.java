package Jogadores;

import logradouros.Empresa;
import logradouros.Imovel;

import java.util.ArrayList;
import java.util.List;

public class Portifolio {
    private double saldo;
    private List<Imovel> imoveis;
    private List<Empresa> empresas;

    public Portifolio(double dinheiroInicial) {
        this.saldo = dinheiroInicial;
        this.imoveis = new ArrayList<>();
        this.empresas = new ArrayList<>();
    }

    public double getSaldo() {
        return saldo;
    }

    public List<Imovel> getImoveis() {
        return imoveis;
    }

    public List<Empresa> getEmpresas() {
        return empresas;
    }

    public void depositar(double quantia) {
        this.saldo += quantia;
    }

    public boolean sacar(double quantia) {
        if (this.saldo >= quantia) {
            this.saldo -= quantia;
            return true;
        }
        return false;
    }

    public void addImovel(Imovel imovel) {
        this.imoveis.add(imovel);
    }

    public void addEmpresa(Empresa empresa) {
        this.empresas.add(empresa);
    }

    public void display() {
        System.out.println("Saldo: $" + String.format("%.2f", saldo));
        System.out.println("Propriedades:");
        if (imoveis.isEmpty()) {
            System.out.println("  Nenhuma propriedade.");
        } else {
            for (Imovel imovel : imoveis) {
                System.out.println("  - " + imovel.getNome());
            }
        }
        System.out.println("Empresas:");
        if (empresas.isEmpty()) {
            System.out.println("  Nenhuma empresa.");
        } else {
            for (Empresa empresa : empresas) {
                System.out.println("  - " + empresa.getNome());
            }
        }
    }
}
