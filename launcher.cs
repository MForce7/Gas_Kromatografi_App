using System;
using System.Diagnostics;
using System.IO;

class Program
{
    static void Main()
    {
        string baseDir = AppContext.BaseDirectory;

        Console.WriteLine(baseDir);

        string python = Path.Combine(baseDir, "Scripts", "python.exe");
        string script = Path.Combine(baseDir, "App", "main.py");

        Console.WriteLine(python);
        Console.WriteLine(script);

        Console.WriteLine(File.Exists(python));
        Console.WriteLine(File.Exists(script));

        try
        {
            Process p = Process.Start(new ProcessStartInfo
            {
                FileName = python,
                Arguments = $"\"{script}\"",
                WorkingDirectory = baseDir,
                UseShellExecute = false,
                CreateNoWindow = false
            });

            Console.WriteLine(p != null ? "Started" : "Failed");
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
        }

        Console.ReadKey();
    }
}