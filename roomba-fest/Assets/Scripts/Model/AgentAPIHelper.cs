using UnityEngine; 
using System.Net;
using System.IO;

public static class AgentAPIHelper
{
    public static Agent GetData()
    {
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create("localhost:8585");

        HttpWebResponse response = (HttpWebResponse)request.GetResponse();

        StreamReader reader = new StreamReader(response.GetResponseStream());

        string json = reader.ReadToEnd();

        return JsonUtility.FromJson<Agent>(json);
    }
}