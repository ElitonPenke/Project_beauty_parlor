import {createTheme} from "@mui/material/styles";
import {purple} from "@mui/material/colors";

export const LightThme= createTheme(
    {
        //isso seria o tem branco
        palette:{
            primary:{
                main: purple[700],
                dark:purple[800] ,
                light:purple[500] ,
                contrastText:"#ffffff",
            },
            secondary:{
                main: purple[500],
                dark:purple[400] ,
                light:purple[300] ,
                contrastText:"#ffffff",
            },
            background:{
                //cor do site em si
                default:"#ffffff",
                //cor de dentro de um card
                paper:"#8d4444",
            }
        }
    }
)