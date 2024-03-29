    using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;
using System.Diagnostics;
using System.IO;
//using System;
using System.Text;

namespace OpenAiCommandHelper
{
    [Rhino.Commands.CommandStyle(Rhino.Commands.Style.ScriptRunner)]
    public class OpenAiCommandHelperCommand : Command
    {
        public OpenAiCommandHelperCommand()
        {
            // Rhino only creates one instance of each command class defined in a
            // plug-in, so it is safe to store a refence in a static property.
            Instance = this;
        }

        ///<summary>The only instance of this command.</summary>
        public static OpenAiCommandHelperCommand Instance { get; private set; }

        ///<returns>The command name as it appears on the Rhino command line.</returns>
        public override string EnglishName => "OpenAiCommandHelperCommand";

        protected override Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            string userInstructions = GetUserInstructions();
            var tokens = userInstructions.Split(new char[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
            RhinoApp.WriteLine($"{tokens.Length}");

            if (string.IsNullOrWhiteSpace(userInstructions) || tokens.Length < 2)
            {
                RhinoApp.WriteLine("No user instructions provided. Aborting.");
                return Result.Failure;
            }
            RhinoApp.RunScript("_-Line 0,0,0 10,10,10", false);

            var ScriptResult = CallPython(userInstructions);
            //RhinoApp.WriteLine(ScriptResult);
            try
            {
                RhinoApp.RunScript(ScriptResult, true);
            }
            catch (Exception e)
            {
                RhinoApp.WriteLine(e.Message);
            }
            return Result.Success;
        }

        private string GetUserInstructions()
        {
            // Implement your logic to obtain user instructions as a string
            // You can use Rhino's GetString or any other method to collect user input
            // For example:
            string prompt = "Enter your instructions in double quotes: ";
            GetString getStr = new Rhino.Input.Custom.GetString();
            getStr.SetCommandPrompt(prompt);

            if (getStr.GetLiteralString() == GetResult.String)
            {
                return getStr.StringResult();
            }
            
            return null; // Return null if user input is canceled
        }

        private string CallPythonScript(string userInstruction)
        {
            string pythonPath = "/opt/homebrew/bin/python3"; // Python path
            string scriptPath = "/Users/shararenorouzi/Library/CloudStorage/GoogleDrive-norouzi.sharare@gmail.com/My Drive/Thesis/call_openai_dep.py"; // Path to your Python script

            ProcessStartInfo start = new ProcessStartInfo
            {
                FileName = pythonPath,
                Arguments = $"\"{scriptPath}\" \"{userInstruction}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    var res = reader.ReadToEnd();
                    RhinoApp.WriteLine(res);

                    RhinoApp.WriteLine("got result!");
                    return res;
                }
            }
        }

        private string CallPython(string userInstruction)
        {
            const string cmd = "bash";
            //const string args = "";
            const string activateConda = "source /Users/shararenorouzi/anaconda3/bin/activate";

            const string activateVenv = "conda activate thesis";
            string scriptPath = "/Users/shararenorouzi/Library/CloudStorage/GoogleDrive-norouzi.sharare@gmail.com/My Drive/Thesis/call_openai.py"; // Path to your Python script

            var pythonCommand = $"python \"{scriptPath}\" \"{userInstruction}\"";
            try {
                var startInfo = new ProcessStartInfo
                {
                    RedirectStandardOutput = true,
                    RedirectStandardInput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    //Arguments = args,
                    FileName = cmd,
                    //WorkingDirectory = workingDirectory
                };
                RhinoApp.WriteLine("trying to run python script!");

                var process = Process.Start(startInfo);
                if (process == null)
                    RhinoApp.WriteLine("Could not start process");

                var sw = process.StandardInput;
                if (sw == null)
                    RhinoApp.WriteLine("Could read the input");

                if (sw.BaseStream.CanWrite)
                {
                    sw.WriteLine(activateConda);

                    sw.WriteLine(activateVenv);
                    RhinoApp.WriteLine("source activated!");
                    sw.WriteLine(pythonCommand);

                    sw.Flush();
                    sw.Close();
                }
                else
                    RhinoApp.WriteLine("Could read the input");

                var sb = new StringBuilder();
                while (!process.HasExited)
                    sb.Append(process.StandardOutput.ReadToEnd());

                var error = process.StandardError.ReadToEnd();
                if (!string.IsNullOrEmpty(error))
                    throw new Exception($"Something went wrong: \n{error}");

                return sb.ToString();
            } catch (Exception e)
            {
                RhinoApp.WriteLine(e.Message);
                return null;
            }
            }

    }
}

