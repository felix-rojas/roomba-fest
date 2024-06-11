using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridInstance : MonoBehaviour
{
    public GameObject web;
    [SerializeField] GameObject wallPrefab; // Prefab del muro
    [SerializeField] GameObject papeleroPrefab; // Prefab del papelero
    [SerializeField] GameObject Trash; // Prefab del papelero
    int height, width;
    string[] initgrid;
    // Start is called before the first frame update
    void SpawnObjects(string[] initgrid)
    {
        height = int.Parse(initgrid[0]);
        
        width = int.Parse(initgrid[1]);
        Debug.Log(width);
        for (int i=2; i<height; i++){
            for (int j=2; j<width; j++){
                if(initgrid[i+j*i] == "X"){
                    //Instance wall vector 3d (i, j,0)
                    Instantiate(wallPrefab, new Vector3(i,0 , j), Quaternion.identity);
                }
                else if(initgrid[i+j*i] == "P"){
                    //Instance papelero
                     Instantiate(papeleroPrefab, new Vector3(i, 0, j), Quaternion.identity);
                }
                else{
                    int number;
                    if(int.TryParse(initgrid[i+j*i], out number)){
                        for(int g=0; g<= number;g++){
                            //Instance wall
                            Instantiate(Trash, new Vector3(i, 0, j), Quaternion.identity);
                        }
                        
                    }
                    
                }
            }
        }
    }
}
