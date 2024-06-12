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
    public GameObject agentPrefab;
    bool alreadyCreated = false;
    public float stepInterval = 2.0f;
    public float stepTimer = 2.0f;

    // IEnumerator - yield return
    IEnumerator SendData(string data)
    {
        WWWForm form = new WWWForm();
        form.AddField("bundle", "the data");
        string url = "http://localhost:8585";
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);
            www.uploadHandler = new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest(); // Talk to Python
            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string jsonData = www.downloadHandler.text;
                List<AgentData> agents = JsonUtility.FromJson<AgentList>("{\"agents\":" + jsonData + "}").agents;
                if (!alreadyCreated)
                {
                foreach (var agentData in agents)
                    {
                        CreateAgent(agentData);
                    }
                alreadyCreated = true;
                
                }
                
                else {
                        foreach (var agentData in agents)
                        {
                            UpdateAgent(agentData, agentData.AgentID);
                        }   
                    }
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
            www.downloadHandler = new DownloadHandlerBuffer();

            yield return www.SendWebRequest(); // Talk to Python
            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
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
        Vector3 fakePos = new Vector3(3.44f, 0, -15.707f);
        string json = EditorJsonUtility.ToJson(fakePos);
        StartCoroutine(GetGridData());
        StartCoroutine(SendData(json));
    }

    // Update is called once per frame
    void Update()
    {
        stepTimer -= Time.deltaTime;
        if (stepTimer <= 0){ StartCoroutine(SendData("hi")); stepTimer = stepInterval ;}
    }

    public void gridInfo(string grid)
    {
        string[] grid_info = grid.Split(",");
        Debug.Log(grid);
        GridInstance.SendMessage("SpawnObjects", grid_info);
    }

    void CreateAgent(AgentData agentData)
    {
        GameObject agent = Instantiate(agentPrefab);
        agent.tag = $"{agentData.AgentID}";
        agent.transform.position = new Vector3(agentData.Position[0], 0, agentData.Position[1]);

        Agent agentComponent = agent.AddComponent<Agent>();
        agentComponent.Carrying = agentData.Carrying;
        agentComponent.AgentID = agentData.AgentID;
        
          Debug.Log($"AgentID: {agentData.AgentID}, Position: ( {agentData.Position[0]}, {agentData.Position[1]} ), Carrying: {agentData.Carrying}");
    }
        void UpdateAgent(AgentData agentData, int id)
    {
        var a = GameObject.FindGameObjectsWithTag($"{id}"); 
        var agent = a[0];

        agent.transform.position = new Vector3(agentData.Position[0], 0, agentData.Position[1]);
        // this could be an error if READ-ONLY        
        // agent.GetComponent<Agent>().Carrying = agentData.Carrying;
        Agent agentComponent = agent.AddComponent<Agent>();
        agentComponent.Carrying = agentData.Carrying;

        var trash_remove_count = agentData.Carrying;
        var trash_list = GameObject.FindGameObjectsWithTag("Trash");
        
            int count = 0;
        foreach (GameObject trash in trash_list)
        {
            Vector3 pos_vec = trash.GetComponent<Transform>().position;
            if (pos_vec.x == agentData.Position[0] && pos_vec.z == agentData.Position[1])
            {
                if (count < trash_remove_count) 
                    { 
                        Destroy(trash);
                        Debug.Log($"Removed trash at {pos_vec.x} , {pos_vec.y}, {pos_vec.z}");
                        count+= 1; 
                        Debug.Log($"Removed {count} trash");
                    }
                else 
                    {
                        count = 0;
                    }
            }
        }
        
          Debug.Log($"AgentID: {agentData.AgentID}, Position: ( {agentData.Position[0]}, {agentData.Position[1]} ), Carrying: {agentData.Carrying}");
    }
}



