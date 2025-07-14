import java.util.*;
import java.io.*;

public class Main {
  private static final boolean DEBUG = Boolean.parseBoolean(System.getProperty("DEBUG", "false"));

  private static void debug(Object... args)  {
    if (DEBUG) {
      System.err.print("DEBUG: ");
      for (Object arg : args) {
        System.err.print(arg + " ");
      }
      System.err.println();
    }
  }

  public static void main(String[] args) throws IOException {
    Scanner sc = new Scanner(System.in);
    // code goes here ...

    sc.close();
  }
}