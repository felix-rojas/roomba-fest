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
        Debug.Log($"{height}, {width}");
        
        for (int i = -1; i < height; i++) {
            Instantiate(wallPrefab, new Vector3(height,0,i), Quaternion.identity);
            Instantiate(wallPrefab, new Vector3(-1,0,i), Quaternion.identity);
}
       for (int i = 0; i <= width; i++) {
            Instantiate(wallPrefab, new Vector3(i,0,width), Quaternion.identity);
            Instantiate(wallPrefab, new Vector3(i,0,-1), Quaternion.identity);
            }
        
        for (int i=2; i<height+2; i++){
            for (int j=2; j<width+2; j++){
                if(initgrid[(i-2)*(j-2)+(i-2)] == "X"){
                    //Instance wall vector 3d (i, j,0)
                    Instantiate(wallPrefab, new Vector3(i-2,0,j-2), Quaternion.identity);
                }
                else if(initgrid[(i-2)*(j-2)+(i-2)] == "P"){
                    //Instance papelero
                     Instantiate(papeleroPrefab, new Vector3(i-2, 0, j-2), Quaternion.identity);
                }
                else{
                    int number;
                    if(int.TryParse(initgrid[(i-2)*(j-2)+(i-2)], out number)){
                        for(int g=0; g< number;g++){
                            //Instance wall
                            if (number > 0) Instantiate(Trash, new Vector3(i-2, g, j-2), Quaternion.identity);
                        }
                        
                    }
                    
                }
            }
        }
    }
}
