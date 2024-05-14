import axios from 'axios';

export interface PredictProps {
    ville: string;
    surface_habitable: number;
    n_pieces: number;
    type_batiment: 'Appartement' | 'Maison'; // Corrected type definition from tuple to union
}

export const predict = async (props: PredictProps) => {
    try {
        const response = await axios.post(
          "http://127.0.0.1:8000/predict",
          props, // Directly pass object instead of a string
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        return JSON.stringify(response.data.prediction);
    } catch (error: any) {
        console.error("Error during API request:", error.response?.data ?? error.message);
        return error.response?.data;
    }
};