file://<WORKSPACE>/Ue01/RekPrime.java
### java.util.NoSuchElementException: next on empty iterator

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 3.3.3
Classpath:
<HOME>/Library/Caches/Coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala3-library_3/3.3.3/scala3-library_3-3.3.3.jar [exists ], <HOME>/Library/Caches/Coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
offset: 449
uri: file://<WORKSPACE>/Ue01/RekPrime.java
text:
```scala
package Ue01;

public class RekPrime {
    public static boolean isPrimeRecursive(int n, int i) {
        if (n <= 1) return false;
        else if (n <= 3) return true;
        else if (n % 2 == 0 || n % 3 == 0) return false;
        else if (i * i > n) return true;
        else if (n % i == 0 || n % (i + 2) == 0) return false;
        else return isPrimeRecursive(n, i + 6);
    }

    public static void main(String[] args) {
        int n1 = 2@@1; // Test with a small number
        System.out.println(n1 + (isPrimeRecursive(n1, 5) ? " is prime." : " is not prime."));

        int n2 = 10007 * 100003; // Test with a large number
        long startTime = System.nanoTime();
        boolean result = isPrimeRecursive(n2, 5);
        long endTime = System.nanoTime();
        double elapsedTime = (endTime - startTime) / 1e9;
        System.out.println(n2 + (result ? " is prime." : " is not prime."));
        System.out.println("Time taken: " + elapsedTime + " s");
    }
}

```



#### Error stacktrace:

```
scala.collection.Iterator$$anon$19.next(Iterator.scala:973)
	scala.collection.Iterator$$anon$19.next(Iterator.scala:971)
	scala.collection.mutable.MutationTracker$CheckedIterator.next(MutationTracker.scala:76)
	scala.collection.IterableOps.head(Iterable.scala:222)
	scala.collection.IterableOps.head$(Iterable.scala:222)
	scala.collection.AbstractIterable.head(Iterable.scala:933)
	dotty.tools.dotc.interactive.InteractiveDriver.run(InteractiveDriver.scala:168)
	scala.meta.internal.pc.MetalsDriver.run(MetalsDriver.scala:45)
	scala.meta.internal.pc.HoverProvider$.hover(HoverProvider.scala:34)
	scala.meta.internal.pc.ScalaPresentationCompiler.hover$$anonfun$1(ScalaPresentationCompiler.scala:368)
```
#### Short summary: 

java.util.NoSuchElementException: next on empty iterator