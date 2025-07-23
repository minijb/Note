---
tags:
  - unity
  - Csharp
---
```c#
using System;
using System.Runtime.InteropServices;

namespace Test
{
    class Program
    {
        static void Main(string[] args)
        {
            ShowMemory();
            doSomething();
            ShowMemory();
        }

        private static void doSomething(){
            ShowMemory();
            A a = new A();
            ShowMemory();

        }
        private static void ShowMemory()
        {
            GC.Collect();
            Console.WriteLine("Memory used : " + GC.GetTotalMemory(true) + "\n");
            Console.WriteLine("---------------------------------------------");
        }
    }
}
public class Inner
{

    string a = "100000000";
    public int b = 100;

}
public struct A
{
    public Inner inner = new Inner(); 
    int i = 100;
    int i1 = 100;

    public A(){

    }
}

// Memory used : 46240

// ---------------------------------------------
// Memory used : 59424

// ---------------------------------------------
// Memory used : 59472

// ---------------------------------------------
// Memory used : 59424

// ---------------------------------------------


```