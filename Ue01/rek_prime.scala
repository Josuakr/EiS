object MainRek extends App {
  def isPrimeRecursive(n: Int, i: Int = 5): Boolean = {
    if (n <= 1) false
    else if (n <= 3) true
    else if (n % 2 == 0 || n % 3 == 0) false
    else if (i * i > n) true
    else if (n % i == 0 || n % (i + 2) == 0) false
    else isPrimeRecursive(n, i + 6)
  }

  val n1 = 13 // Test with a small number
  println(if (isPrimeRecursive(n1)) s"$n1 is prime." else s"$n1 is not prime.")

  val n2 = 10007 * 100003 // Test with a large number
  val startTime = System.nanoTime()
  val result = isPrimeRecursive(n2)
  val endTime = System.nanoTime()
  val elapsedTime = (endTime - startTime) / 1e9
  println(if (result) s"$n2 is prime." else s"$n2 is not prime.")
  println(s"Time taken: $elapsedTime s")
}
