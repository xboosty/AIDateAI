/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package python;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 *
 * @author ADRIEL WORKS
 */
public class RunScriptPython {
    private String pathScriptApi;
    private String pathPython;

    public RunScriptPython(String pathScriptApi, String pathPython) {
        this.pathScriptApi = pathScriptApi;
        this.pathPython = pathPython;
    }
    
    
    public void createNewPresentation(String presentation){
        presentation = presentation.replace(" ", "-");
        String command = pathPython +" " + pathScriptApi + " createNewPresentation " + presentation;
        runConsoleCommand(command);
    }
    
    public void speakPresentation(){         
        String command = pathPython +" " + pathScriptApi + " speakPresentation";
        runConsoleCommand(command);
    }
    
    public void createPathPresentation(String path){    
        String command = pathPython +" " + pathScriptApi + " setPathPresentation "+path;
        System.out.println(command);
        runConsoleCommand(command);
    }
    
    public void createPathRoot(String path){    
        String command = pathPython +" " + pathScriptApi + " createPathRoot "+path;
        runConsoleCommand(command);
    }
    
    public void runConsoleCommand(String command){
        try {          
            //ProcessBuilder builder = new ProcessBuilder(command);

            // Establece el directorio de trabajo si es necesario
            //builder.directory(new File("F:\\NTSprint\\work\\AIDateAI\\AIDateAI\\projects\\assistant_enterview"));

            // Inicia el proceso
            //Process process = builder.start();
            Process process = Runtime.getRuntime().exec(command);
            // Captura la salida estándar (stdout) del proceso
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

            // Captura la salida de error estándar (stderr) del proceso
            BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            
            // Espera a que el proceso termine
            int result = process.waitFor();

            // Imprime el resultado
            if (result == 0) {
                System.out.println("Run script Python with sucess.");
            } else {
                System.out.println("Run script Python ended with an error. Error details:");
                String errorLine;
                while ((errorLine = stdError.readLine()) != null) {
                    System.out.println(errorLine);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        
    }
    
}
