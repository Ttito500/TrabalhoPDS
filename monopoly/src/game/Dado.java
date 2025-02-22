package game;

import java.util.Random;

public class Dado {
    private Random random;

    public Dado() {
        this.random = new Random();
    }

    public int roll() {
        return random.nextInt(6) + 1 + random.nextInt(6) + 1; // 2 dados de 6 lados
    }
}
