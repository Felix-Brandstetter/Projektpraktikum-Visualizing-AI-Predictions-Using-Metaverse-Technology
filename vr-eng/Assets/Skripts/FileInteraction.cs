using System;
using System.Threading.Tasks;
using UnityEngine;

#if UNITY_WSA && !UNITY_EDITOR
using Windows.Storage;
#else
using System.IO;
#endif
public class FileInteraction
{
    public static async Task<string> Load(string csvFile)
    {
        string data = null;

#if UNITY_WSA && !UNITY_EDITOR
            try
            {
                StorageFolder fLocal = ApplicationData.Current.LocalFolder;

                StorageFile file = await fLocal.GetFileAsync(csvFile);
                if (file != null) {
                    data = await FileIO.ReadTextAsync(file);
                }
            } catch {
            }
#else

        // Win32
        var documents = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);

        // Create folder if it doesnt exist
        //Directory.CreateDirectory(Path.Combine(documents, "MVP Daten", "Personen CSV"));
        var path = Path.Combine(documents, "MVP Daten", csvFile);
        // Read from file
        if (File.Exists(path))
        {
            data = File.ReadAllText(path);
        }
#endif
        if (data == null || data.Length == 0)
        {
            return null;
        }
        else
        {
            return data;
        }
    }
}
