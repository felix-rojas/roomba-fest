using UnityEngine; 
using System.Net;
using System.IO;

public static class AgentAPIHelper
{
    public static Agent GetData()
    {
        HttpWebRequest request = (HttpWebRequest)WebRequest.Create("http://localhost:8585/");

        HttpWebResponse response = (HttpWebResponse)request.GetResponse();

        StreamReader reader = new(response.GetResponseStream());

        string json = reader.ReadToEnd();

        Debug.Log(json);

        return JsonUtility.FromJson<Agent>(json);
    }
}