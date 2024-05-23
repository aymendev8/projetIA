import { Button, Card, Form, FormProps, InputNumber, Select, Spin } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import "./App.css";
import { useState } from "react";
import { predict } from "./api/Api";

type PredictProps = {
  ville: string;
  surface_habitable: number;
  n_pieces: number;
  type_batiment: "Appartement" | "Maison"; // Corrected type definition
};

const big_cities = [
  { label: "Paris", value: "PARIS" },
  { label: "Marseille", value: "MARSEILLE" },
  { label: "Lyon", value: "LYON" },
  { label: "Toulouse", value: "TOULOUSE" },
  { label: "Nice", value: "NICE" },
  { label: "Nantes", value: "NANTES" },
  { label: "Montpellier", value: "MONTPELLIER" },
  { label: "Bordeaux", value: "BORDEAUX" },
  { label: "Lille", value: "LILLE" },
  { label: "Rennes", value: "RENNES" },
  { label: "Reims", value: "REIMS" },
  { label: "Toulon", value: "TOULON" },
  { label: "Le Havre", value: "LE HAVRE" },
  { label: "Grenoble", value: "GRENOBLE" },
  { label: "Dijon", value: "DIJON" },
  { label: "Angers", value: "ANGERS" },
  { label: "Nîmes", value: "NIMES" },
  { label: "Villeurbanne", value: "VILLEURBANNE" },
  { label: "Saint-Denis", value: "SAINT-DENIS" },
  { label: "Le Mans", value: "LE MANS" },
  { label: "Brest", value: "BREST" },
  { label: "Tours", value: "TOURS" },
  { label: "Amiens", value: "AMIENS" },
  { label: "Limoges", value: "LIMOGES" },
  { label: "Perpignan", value: "PERPIGNAN" },
  { label: "Besançon", value: "BESANCON" },
  { label: "Orléans", value: "ORLEANS" },
  { label: "Annemasse", value: "ANNEMASSE" },
  { label: "Rouen", value: "ROUEN" },
  { label: "Avignon", value: "AVIGNON" },
  { label: "Paris 1er", value: "PARIS 01" },
  { label: "Paris 2e", value: "PARIS 02" },
  { label: "Paris 3e", value: "PARIS 03" },
  { label: "Paris 4e", value: "PARIS 04" },
  { label: "Paris 5e", value: "PARIS 05" },
  { label: "Paris 6e", value: "PARIS 06" },
  { label: "Paris 7e", value: "PARIS 07" },
  { label: "Paris 8e", value: "PARIS 08" },
  { label: "Paris 9e", value: "PARIS 09" },
  { label: "Paris 10e", value: "PARIS 10" },
  { label: "Paris 11e", value: "PARIS 11" },
  { label: "Paris 12e", value: "PARIS 12" },
  { label: "Paris 13e", value: "PARIS 13" },
  { label: "Paris 14e", value: "PARIS 14" },
  { label: "Paris 15e", value: "PARIS 15" },
  { label: "Paris 16e", value: "PARIS 16" },
  { label: "Paris 17e", value: "PARIS 17" },
  { label: "Paris 18e", value: "PARIS 18" },
  { label: "Paris 19e", value: "PARIS 19" },
  { label: "Paris 20e", value: "PARIS 20" },
  { label: "Marseille 1er", value: "MARSEILLE 1ER" },
  { label: "Marseille 2e", value: "MARSEILLE 2EME" },
  { label: "Marseille 3e", value: "MARSEILLE 3EME" },
  { label: "Marseille 4e", value: "MARSEILLE 4EME" },
  { label: "Marseille 5e", value: "MARSEILLE 5EME" },
  { label: "Marseille 6e", value: "MARSEILLE 6EME" },
  { label: "Marseille 7e", value: "MARSEILLE 7EME" },
  { label: "Marseille 8e", value: "MARSEILLE 8EME" },
  { label: "Marseille 9e", value: "MARSEILLE 9EME" },
  { label: "Marseille 10e", value: "MARSEILLE 10EME" },
  { label: "Marseille 11e", value: "MARSEILLE 11EME" },
  { label: "Marseille 12e", value: "MARSEILLE 12EME" },
  { label: "Marseille 13e", value: "MARSEILLE 13EME" },
  { label: "Marseille 14e", value: "MARSEILLE 14EME" },
  { label: "Marseille 15e", value: "MARSEILLE 15EME" },
  { label: "Marseille 16e", value: "MARSEILLE 16EME" },
  { label: "Lyon 1er", value: "LYON 1ER" },
  { label: "Lyon 2e", value: "LYON 2EME" },
  { label: "Lyon 3e", value: "LYON 3EME" },
  { label: "Lyon 4e", value: "LYON 4EME" },
  { label: "Lyon 5e", value: "LYON 5EME" },
  { label: "Lyon 6e", value: "LYON 6EME" },
  { label: "Lyon 7e", value: "LYON 7EME" },
  { label: "Lyon 8e", value: "LYON 8EME" },
  { label: "Lyon 9e", value: "LYON 9EME" },
];

function App() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<string | null>(null);

  const onFinish: FormProps<PredictProps>["onFinish"] = (values) => {
    console.log("Success:", values);
    setLoading(true);
    predict(values)
      .then((response) => {
        setPrediction(response);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setLoading(false);
      });
  };

  const onFinishFailed: FormProps<PredictProps>["onFinishFailed"] = (
    errorInfo
  ) => {
    console.log("Failed:", errorInfo);
  };

  // Filter `option.label` match the user type `input`
  const filterOption = (
    input: string,
    option?: { label: string; value: string }
  ) => (option?.label ?? "").toLowerCase().includes(input.toLowerCase());

  return (
    <>
      <section>
        <Form
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          layout="vertical"
        >
          <Form.Item
            label="Ville"
            name="ville"
            rules={[{ required: true, message: "Please input your city!" }]}
          >
            <Select
              showSearch
              placeholder="Select a city"
              optionFilterProp="children"
              filterOption={filterOption}
              options={big_cities}
            />
          </Form.Item>
          <Form.Item
            label="Surface habitable (m²)"
            name="surface_habitable"
            rules={[
              { required: true, message: "Please fill in the living area!" },
            ]}
          >
            <InputNumber />
          </Form.Item>
          <Form.Item
            label="Nombre de pièces"
            name="n_pieces"
            rules={[
              { required: true, message: "Please input the number of rooms!" },
            ]}
          >
            <InputNumber />
          </Form.Item>
          <Form.Item
            label="Type de bâtiment"
            name="type_batiment" // Corrected field name
            rules={[
              {
                required: true,
                message: "Please select the type of building!",
              },
            ]}
          >
            <Select>
              <Select.Option value="Appartement">Appartement</Select.Option>
              <Select.Option value="Maison">Maison</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item
            wrapperCol={{
              offset: 10,
              span: 16,
            }}
          >
            <Button
              type="primary"
              icon={<SearchOutlined />}
              htmlType="submit"
              children="Estimer"
            />
          </Form.Item>
        </Form>
      </section>
      <section>
        <Card title="Résultat" style={{ width: 300 }}>
          {loading ? (
            <Spin />
          ) : (
            <p>
              {prediction
                ? "Votre bien est estimé à " +
                  Math.round(+prediction).toLocaleString("fr-FR") +
                  "€ !"
                : "Rentrer votre recherche"}
            </p>
          )}
        </Card>
      </section>
    </>
  );
}

export default App;
