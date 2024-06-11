// TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
// C# client to interact with Python server via POST
// Sergio Ruiz-Loza, Ph.D. March 2021

using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class WebClient : MonoBehaviour
{
    public GameObject GridInstance;
    // IEnumerator - yield return
    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
            //www.SetRequestHeader("Content-Type", "text/html");
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();          // Talk to Python
            if((www.result == UnityWebRequest.Result.ConnectionError) || ((www.result == UnityWebRequest.Result.ProtocolError)))
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log(www.downloadHandler.text);
                //writeObject(text_thing);
                //var data_res = JsonUtility.FromJson<DataModel>(www.downloadHandler.text);
                //Debug.Log(data_res);
                //Debug.Log("Form upload complete!");
            }
        }

    }

    // IEnumerator - yield return
    IEnumerator GetGridData()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8585";
        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

            yield return www.SendWebRequest();          // Talk to Python
            if((www.result == UnityWebRequest.Result.ConnectionError) || ((www.result == UnityWebRequest.Result.ProtocolError)))
            {
                Debug.Log(www.error);
            }
            else
            {
                gridInfo(www.downloadHandler.text);
            }
        }

    }


    // Start is called before the first frame update
    void Start()
    {
        //string call = "What's up?";
        Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        string json = EditorJsonUtility.ToJson(fakePos);
        
        //StartCoroutine(SendData(call));
        StartCoroutine(GetGridData());
        StartCoroutine(SendData(json));
        // transform.localPosition
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    
    public string[] gridInfo(string grid){
    //Debug.Log($"{grid}");
    string[] grid_info = grid.Split(",");
    GridInstance.SendMessage("SpawnObjects", grid_info);
    return grid_info;
    
}
    
}
