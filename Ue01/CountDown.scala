@main def CountDown = { // Syntax kept close to JAVA 
    for (i <- 10 to 1 by -1) { // (for simplicity)
        println(i);
        if (i == 8) {
            println("ignition sequence start"); 
        }
    }
    println("liftoff!");
}