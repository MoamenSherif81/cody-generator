//
// Created by ziad on 3/1/25.
//

#include <filesystem>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>
// install nlohmann/json.hpp
#include "nlohmann/json.hpp"
#include <random>
using namespace std;

void load_rules(const string &rules_location, unordered_map<string, bool> &is_term,
                unordered_map<string, vector<string>> &children, unordered_map<string, bool> &consecutive)
{
    ifstream file(rules_location);
    if (!file.is_open())
    {
        throw runtime_error("Could not open DSL rules file: " + rules_location);
    }

    nlohmann::json rules;
    file >> rules;

    for (auto &[key, value] : rules.items())
    {
        is_term[key] = value["term"];
        consecutive[key] = value["consecutive"];
        for (const auto &child : value["children"])
        {
            children[key].push_back(child);
        }
    }
}

void generate(const string &cur_node, string &dsl, mt19937 &rng, unordered_map<string, bool> &is_term,
              unordered_map<string, vector<string>> &children, unordered_map<string, bool> &consecutive, string &last)
{
    if (is_term[cur_node])
    {
        dsl += cur_node;
        last = cur_node;
    }
    if (children[cur_node].empty())
    {
        return;
    }
    if (is_term[cur_node])
    {
        dsl += "{";
    }

    int num_children = 1;
    if (cur_node == "root" or is_term[cur_node])
    {
        num_children = uniform_int_distribution(1, 2)(rng);
    }
    for (int i = 0; i < num_children; i++)
    {
        const string to = children[cur_node][uniform_int_distribution(0, (int)children[cur_node].size() - 1)(rng)];
        if (to == last and !consecutive[to])
        {
            i--;
            continue;
        }
        generate(to, dsl, rng, is_term, children, consecutive, last);
        if (i + 1 != num_children)
        {
            dsl += ",";
        }
    }
    if (is_term[cur_node])
    {
        dsl += "}";
    }
}

signed main(int argc, char *argv[])
{
    if (argc < 6)
    {
        cerr << "Need 5 arguments: number of samples, folder location, file counter, rules location, and seed\n";
        return 1;
    }

    try
    {
        unordered_map<string, vector<string>> children;
        unordered_map<string, bool> is_term;
        unordered_map<string, bool> consecutive;
        unsigned int num_samples = atoi(argv[1]);
        string folder_location = argv[2];
        unsigned int file_counter = atoi(argv[3]);
        string rules_location = argv[4];
        unsigned int seed = atoi(argv[5]);

        load_rules(rules_location, is_term, children, consecutive);

        mt19937 rng(seed);

        for (int i = 0; i < num_samples; i++)
        {
            ofstream file(folder_location + "/" + to_string(file_counter++) + ".gui");
            string content, last;
            generate("root", content, rng, is_term, children, consecutive, last);
            file << content;
        }
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error " << e.what() << "\n";
        return 1;
    }

    return 0;
}
