var _debug = false;
fun <T> debug(vararg vals: T): Unit {
    if (!_debug) { return }
    for (v in vals) { System.err.print(v); System.err.print(" ") }
    System.err.println()
}

fun main(args: Array<String>) {
    if (args.size > 0 && args[0] == "-d") {
        _debug = true;
    }

    val n = readLine()!!.toInt()
    val (a, b) = readLine()!!.split(' ').map(String::toLong)
}
