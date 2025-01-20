import os
import numpy as np
import matplotlib.pyplot as plt


def translate_stats_log(file_path):
    translate_map = {
        "psi.height": "treeheight",
        "psi.treeLength": "treelength"
    }
    count = 10
    for i in range(count):
        var_name = "pi." + str(i)
        translate_map[var_name] = var_name.replace(".", "_")
    for i in ["a", "b", "c", "d", "e", "f"]:
        var_name = "pi." + i
        translate_map[var_name] = "pi_" + str(count)
        count += 1
    rate_names = ["AC", "AG", "AT", "CG", "CT", "GT"]
    for i in range(len(rate_names)):
        var_name = "rates." + rate_names[i]
        var_name_new = "rates_" + str(i)
        translate_map[var_name] = var_name_new
    if os.path.exists(file_path + ".orig"):
        return
    os.rename(file_path, file_path + ".orig")
    writer = open(file_path, 'w')
    with open(file_path + ".orig", 'r') as reader:
        header_line = reader.readline().strip()
        headers = header_line.split('\t')
        for i in range(len(headers)):
            if headers[i] in translate_map:
                headers[i] = translate_map[headers[i]]
        writer.write("\t".join(headers) + "\n")
        for data_line in reader:
            writer.write(data_line)
    writer.close()


def translate_all_stats_logs(filepath):
    for i in range(100):
        translate_stats_log(filepath % i)


def parse_true_csv(file_path):
    sep = "\t"
    with open(file_path, 'r') as reader:
        header_line = reader.readline().strip()
        data_line = reader.readline().strip()
        headers = header_line.split(sep)
        data = data_line.split(sep)
        zipped_data = zip(headers, data)
        result = {}
        for header, data in zipped_data:
            try:
                result[header] = float(data)
            except ValueError:
                result[header] = data
        return result


def parse_stats_log(file_path):
    with open(file_path, 'r') as reader:
        result = {}
        header_line = reader.readline().strip()
        headers = header_line.split('\t')[1:]
        for data_line in reader:
            data_line = data_line.strip()
            items = data_line.split('\t')
            trace = items[0]
            if trace == "mode":
                continue
            items = items[1:]
            zipped_data = zip(headers, items)
            tmp = {}
            for header, data in zipped_data:
                tmp[header] = float(data)
            result[trace] = tmp
    return result


def calculate_r2(true_values, mean_values):
    correlation_matrix = np.corrcoef(true_values, mean_values)
    correlation_xy = correlation_matrix[0, 1]
    r_squared = correlation_xy ** 2
    return r_squared


def plot_figs(stats_path, true_path, parameter_list):
    true = []
    mean = []
    hdp95lower = []
    hdp95upper = []
    ess = []
    outside_95_info = {parameter: [] for parameter in parameter_list}
    max_f0 = float('-inf')  # Initialize max f0
    # translate stats logs
    translate_all_stats_logs(stats_path)
    # convert parameters to math characters
    parameter_map = {
        "delta": r"$\delta$",
        "epsilon": r"$\epsilon$",
        "treeheight": "tree height",
        "treelength": "tree length",
        "pi_0": r"$\pi_{AA}$",
        "pi_1": r"$\pi_{AC}$",
        "pi_2": r"$\pi_{AG}$",
        "pi_3": r"$\pi_{AT}$",
        "pi_4": r"$\pi_{CA}$",
        "pi_5": r"$\pi_{CC}$",
        "pi_6": r"$\pi_{CG}$",
        "pi_7": r"$pi_{CT}$",
        "pi_8": r"$\pi_{GA}$",
        "pi_9": r"$\pi_{GC}$",
        "pi_10": r"$\pi_{GG}$",
        "pi_11": r"$\pi_{GT}$",
        "pi_12": r"$\pi_{TA}$",
        "pi_13": r"$\pi_{TC}$",
        "pi_14": r"$\pi_{TG}$",
        "pi_15": r"$\pi_{TT}$",
        "rates_0": r"$r_{AC}$",
        "rates_1": r"$r_{AG}$",
        "rates_2": r"$r_{AT}$",
        "rates_3": r"$r_{CG}$",
        "rates_4": r"$r_{CT}$",
        "rates_5": r"$r_{GT}$",
        "f0": "f0",
        "N0": "N0",
        "b": "b"
    }
    # figure settings
    font_size = 12
    width = 6.75 / 2
    plt.rcParams['font.family'] = 'Helvetica'
    plt.rc('font', size=font_size)
    plt.rc('axes', titlesize=font_size)
    plt.rcParams['figure.figsize'] = (width, width)
    plt.rcParams['figure.dpi'] = 300
    # process files
    for fileid in range(100):
        stats_file = stats_path % fileid
        true_file = true_path % fileid
        stats_data = parse_stats_log(stats_file)
        true_data = parse_true_csv(true_file)
        mean.append(stats_data['mean'])
        hdp95lower.append(stats_data['HPD95.lower'])
        hdp95upper.append(stats_data['HPD95.upper'])
        ess.append(stats_data['ESS'])
        true.append(true_data)
        # Update max_f0 if the current f0 is greater
        if 'f0' in true_data:
            max_f0 = max(max_f0, true_data['f0'])
    # calculate correlation and R2
    correlations = {}
    r2_values = {}
    for parameter in parameter_list:
        try:
            true_values = [x[parameter] for x in true]
            mean_values = [x[parameter] for x in mean]
            if len(true_values) > 0 and len(mean_values) > 0:
                correlation = np.corrcoef(true_values, mean_values)[0, 1]
                correlations[parameter] = correlation
                r2 = calculate_r2(true_values, mean_values)
                r2_values[parameter] = r2
        except KeyError:
            print(f"Parameter {parameter} not found in data.")
    # plot parameters
    for parameter in parameter_list:
        # get values
        try:
            true_values = [x[parameter] for x in true]
            mean_values = [x[parameter] for x in mean]
            lowers = [x[parameter] for x in hdp95lower]
            uppers = [x[parameter] for x in hdp95upper]
            ess_values = [x[parameter] for x in ess]
            mapped_parameter = parameter_map[parameter]
            # map colors
            color_list = {True: 'c', False: 'r'}
            colors_boolean = [lowers[i] <= true_values[i] <= uppers[i] for i in range(len(true_values))]
            color_values = [color_list[x] for x in colors_boolean]
            # record outside 95% HPD
            for i, within in enumerate(colors_boolean):
                if not within:
                    outside_95_info[parameter].append((i, ess_values[i], true_values[i]))
            # begin plotting
            plt.clf()
            line_width = 3
            alpha = 0.2
            ax = plt.subplot(111)
            plt.plot(true_values, mean_values, 'k.', ms=2, zorder=2)
            plt.vlines(true_values, ymin=lowers, ymax=uppers, colors=color_values, alpha=alpha, lw=line_width, zorder=1)
            if parameter == "treeheight" or parameter == "treelength":
                plt.plot([0, max(true_values)], [0, max(true_values)], 'k-', lw=0.5, label="x = y", zorder=10)
            else:
                y1 = min(lowers)
                y2 = max(uppers)
                x1 = min(true_values)
                x2 = max(true_values)
                plt.plot([x1, x2], [x1, x2], 'k-', lw=0.5, label="x = y", zorder=10)
            plt.xlabel("True " + parameter_map[parameter])
            plt.ylabel("Estimated " + parameter_map[parameter])
            plt.title(parameter_map[parameter])
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            plt.tight_layout()
            within_hpd_count = sum(
                lower <= true_val <= upper for true_val, lower, upper in zip(true_values, lowers, uppers)
            )
            total_count = len(true_values)
            coverage_percent = within_hpd_count / total_count * 100
            plt.text(
                0.05, 0.95,
                f'covg. = {coverage_percent:.0f} %\ncorr. = {correlations[parameter]:.2f}\nR2 = {r2_values[parameter]:.2f}\nESS = {np.mean(ess_values):.2f}',
                transform=plt.gca().transAxes,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='left',
                bbox=dict(facecolor='white', alpha=0.5)
            )
            output_path = "/Users/xuyuan/workspace/PopFunc-paper/gompertz_f0/gt16/figures/" + parameter.lower().replace(".",
                                                                                                                "_") + ".pdf"
            plt.savefig(output_path)
            print("figure saved: %s" % os.path.abspath(output_path))
        except KeyError:
            print(f"Parameter {parameter} not found in data.")

    # Output outside 95% HPD info
    for parameter in parameter_list:
        if outside_95_info[parameter]:
            print(f"\nParameter {parameter} outside 95% HPD:")
            for file_index, ess_value, true_value in outside_95_info[parameter]:
                print(f"File index: {file_index}, ESS: {ess_value}, True Value: {true_value}")

    # Print the max f0 value
    print(f"\nMax f0 value: {max_f0}")


# gt16 simulation 3
parameters = ["f0", "N0", "b", "treeheight", "treelength", "delta", "epsilon", "pi_0", "pi_1", "pi_2", "pi_3",
              "pi_4", "pi_5", "pi_6", "pi_7", "pi_8", "pi_9", "pi_10", "pi_11", "pi_12", "pi_13", "pi_14",
              "pi_15", "rates_0", "rates_1", "rates_2", "rates_3", "rates_4", "rates_5"]
stats_format = "/Users/xuyuan/workspace/PopFunc-paper/gompertz_f0/gt16/stats/gompCoal-%d_stats.log"
true_format = "/Users/xuyuan/workspace/PopFunc-paper/gompertz_f0/gt16/data/gompCoal-%d.log"
plot_figs(stats_format, true_format, parameters)



