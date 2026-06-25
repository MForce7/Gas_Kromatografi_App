using System;
using System.Diagnostics;
using System.IO;

class Program
{
    static void Main()
    {
        string baseDir = AppContext.BaseDirectory;

        string python = Path.Combine(baseDir, "Scripts", "python.exe");
        string script = Path.Combine(baseDir, "App", "main.py");

        Process.Start(new ProcessStartInfo
        {
            FileName = python,
            Arguments = $"\"{script}\"",
            WorkingDirectory = baseDir,
            UseShellExecute = false,
            CreateNoWindow = true
        });
    }
}