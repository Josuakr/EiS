object Main extends App {
  def isPrime(n: Int): Boolean = {
    if (n <= 1) return false
    if (n <= 3) return true
    if (n % 2 == 0 || n % 3 == 0) return false
    var i = 5
    while (i * i <= n) {
      if (n % i == 0 || n % (i + 2) == 0) return false
      i += 6
    }
    true
  }

  val n = 10007 * 100003
  val startTime = System.nanoTime()
  val result = isPrime(n)
  val endTime = System.nanoTime()
  val elapsedTime = (endTime - startTime) / 1e9
  if (result) {
    println(s"$n is prime.")
  } else {
    println(s"$n is not prime.")
  }
  println(s"Time taken: $elapsedTime s")
}
