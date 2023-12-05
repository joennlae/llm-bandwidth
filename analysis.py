import os, yaml

import pandas as pd
import matplotlib.pyplot as plt


def read_in_results(folder="./results"):
    # check if the folder exists
    if not os.path.exists(folder):
        raise ValueError(f"Folder {folder} does not exist.")

    bandwidth_results = []
    model_results = []

    if os.path.exists(os.path.join(folder, "bandwidth/output.csv")):
        # read file in with python as text
        bandwidth_results = {}
        with open(os.path.join(folder, "bandwidth/output.csv"), "r") as f:
            lines = f.readlines()
            type = "no_type"
            current_lines = []
            for line in lines[1:]:
                line = line.strip()
                # check if line starts with a number (i.e. a timestamp)
                if line[0].isdigit():
                    amount = int(line.split(",")[0])
                    speed = float(line.split(",")[1])
                    row = {
                        "amount": amount / 1024 / 1024,  # bytes to MB
                        "speed": speed,
                    }
                    current_lines.append(row)
                else:
                    if type != "no_type":
                        bandwidth_results[type] = current_lines
                    type = line
                    bandwidth_results[type] = []
                    current_lines = []
                bandwidth_results[type] = current_lines

    for key in bandwidth_results.keys():
        bandwidth_results[key] = pd.DataFrame(bandwidth_results[key])

    # create a 2d index for the bandwidth results
    print(bandwidth_results)

    if os.path.exists(os.path.join(folder, "models")):
        # get all folders in the models folder
        model_folders = os.listdir(os.path.join(folder, "models"))
        print(model_folders)
        for model_folder in model_folders:
            # get all files in the model folder
            batch_size = int(model_folder.split("-")[0])
            n_predictions = int(model_folder.split("-")[1])
            context_size = int(model_folder.split("-")[2])
            model_name = "".join(model_folder.split("-")[3:])

            print("values", batch_size, n_predictions, context_size, model_name)

            # read yml result file
            # get files in folder
            files = os.listdir(os.path.join(folder, "models", model_folder))
            # get yml file
            yml_file = [f for f in files if f.endswith(".yml")][0]
            # read in yml file
            dict_keys_to_store = [
                "threads",
                "top_k",
                "top_p",
                "numa",
                "mst_eval",
                "mst_p_eval",
                "mst_sample",
                "n_eval",
                "n_p_eval",
                "n_sample",
                "t_eval_us",
                "t_load_us",
                "t_p_eval_us",
                "t_sample_us",
                "ts_eval",
                "ts_p_eval",
                "ts_sample",
            ]
            results = {
                "batch_size": batch_size,
                "n_predictions": n_predictions,
                "context_size": context_size,
                "model_name": model_name,
            }
            with open(os.path.join(folder, "models", model_folder, yml_file), "r") as f:
                # read full file into string
                file_str = f.read()
                # replace illegal escape characters that can happen in output
                file_str = file_str.replace("\\i", "\\\\i")
                yml = yaml.load(file_str, Loader=yaml.FullLoader)
                for store_key in dict_keys_to_store:
                    results[store_key] = yml[store_key]
            model_results.append(results)
    print(model_results)
    model_results = pd.DataFrame(model_results)
    print(model_results)

    # replace nan in model results
    model_results = model_results.replace("-nan", 0.0)

    # store model results
    model_results.to_csv(os.path.join(folder, "models.csv"), index=False)


def plotting(folder="./results"):
    # load csv pandas
    model_results = pd.read_csv("./results/models.csv")
    # plot model results
    context_size = 2048
    n_predictions = 512
    # sort dataframe by model name
    model_results = model_results.sort_values(by=["model_name", "batch_size"])
    # color
    for model_name in model_results["model_name"].unique():
        print(model_name)
        # add data to plot
        data = model_results[
            (model_results["model_name"] == model_name)
            & (model_results["context_size"] == context_size)
            & (model_results["n_predictions"] == n_predictions)
            & (model_results["batch_size"] >= 2)
        ]
        # plt.plot(
        #     data["batch_size"].to_numpy(),
        #     data["ts_eval"].to_numpy(),
        #     label="token/s generation",
        #     marker="x",
        # )
        plt.plot(
            data["batch_size"].to_numpy(),
            data["ts_p_eval"].to_numpy(),
            label="token/s generation",
            marker="o",
        )
    plt.title("Token Generation Speed")
    # x log scale
    plt.xscale("log")
    plt.xticks(
        data["batch_size"].to_numpy(),
        [str(elem) for elem in data["batch_size"].to_numpy()],
        minor=False,
    )
    # x ticks
    plt.ylabel("token/s")
    plt.xlabel("batch size")
    # plt.savefig(os.path.join(folder, f"{model_name}.png"))
    # plt.close()
    plt.savefig(os.path.join(folder, f"all.png"))
    plt.close()


if __name__ == "__main__":
    # read_in_results()
    plotting()
