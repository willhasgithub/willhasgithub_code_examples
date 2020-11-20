"""
In one project I needed was tasked with creating a higher level object for the sales team to denote an organization.
The database is structured (bottom down) website --> account --> contact

There are many accounts to a single website (treated like an office without a headquarters identified)
and many contacts to a single account.

Websites are used to group accounts but the people who made the database did not factor in for websites changing.
They put a temporary solution where they would periodically check the website for a redirect.
If there is one, the CRM will automatically create a new website record and populate a field on the original website
as a redirect to the new one.
The account below is not changed. It still points to the old website.

The leadership team is asking for a solution which allows them to keep the old data (original website on the account level).

We can utilize the given property that any website can only point to ONE other website redirect.
Therefore, with a directional graph there can be at worst a loop (many parents) with one trailing string (acestors)
and typically will be a string of pointers ending at single website (single parent).

Therefore, we can cluster these groups and make a very good guess at the parent website.

We can then create an organization object which corresponds to these clusters. This program will run periodically,
identify the parents, and label the organizations and populate that value down to the account level for easier reporting.

Below is the driver to do that.
I have removed the main method here since it contains important information to the
structure of the warehouse via SQL queries and update statements
"""


import networkx as nx


class ParentsDictProxy:
    def __init__(self, website_rankings_selection):
        selection_dictionary = {row[0]: list(row[1:6]) for row in website_rankings_selection}

        directed_graph = self.make_directed_graph(selection_dictionary)
        self.label_parents(directed_graph)
        self.label_related_parents(directed_graph)

        self.parents_dictionary = self.construct_parents_dictionary(directed_graph)
        pass

    @staticmethod
    def make_directed_graph(selection_dictionary):
        directed_graph = nx.DiGraph()
        for website_ranking_id, attributes in selection_dictionary.items():
            website_ranking_name = attributes[0]
            bool_generic_domain, bool_redirect = attributes[1], attributes[2]
            redirect_id, redirect_name = attributes[3], attributes[4]

            directed_graph.add_node(website_ranking_id, name=website_ranking_name, is_parent=False,
                                    is_generic=bool_generic_domain)
            if bool_redirect:
                red_is_generic = selection_dictionary[redirect_id][1]
                directed_graph.add_node(redirect_id, name=redirect_name, is_parent=False, is_generic=red_is_generic)
                directed_graph.add_edge(website_ranking_id, redirect_id)
        return directed_graph

    @staticmethod
    def label_parents(directed_graph):
        website_rankings = list(directed_graph.nodes)
        for website_ranking in website_rankings:
            wr_has_successor = len(list(directed_graph.successors(website_ranking))) > 0
            if wr_has_successor:
                target = website_ranking
                examined_list = []
                while True:
                    examined_list.append(target)

                    target_has_successor = len(list(directed_graph.successors(target))) > 0
                    if target_has_successor:
                        target_succssor = list(directed_graph.successors(target))[0]

                        if target_succssor in examined_list:
                            if target_succssor == website_ranking:
                                directed_graph.nodes[website_ranking]['is_parent'] = True
                                ancestors = nx.ancestors(directed_graph, website_ranking)
                                if ancestors:
                                    directed_graph.nodes[website_ranking]["ancestors"] = nx.ancestors(directed_graph,
                                                                                                      website_ranking)
                            break
                        target = target_succssor
                    else:
                        break
            else:
                directed_graph.nodes[website_ranking]['is_parent'] = True
                ancestors = nx.ancestors(directed_graph, website_ranking)
                if ancestors:
                    directed_graph.nodes[website_ranking]["ancestors"] = nx.ancestors(directed_graph, website_ranking)

    @staticmethod
    def find_nearest_parent(directed_graph, domain):
        target = domain
        is_parent = directed_graph.nodes[domain]["is_parent"]
        while is_parent is False:
            target = list(directed_graph.successors(target))[0]
            is_parent = directed_graph.nodes[target]["is_parent"]
        return target

    # will be used for SF data
    @staticmethod
    def find_all_related_parents(directed_graph, domain):
        parents = []
        is_parent = directed_graph.nodes[domain]["is_parent"]

        if is_parent:
            parents.append(domain)

        descendants = nx.descendants(directed_graph, domain)
        if descendants:
            for descendant in descendants:
                is_parent = directed_graph.nodes[descendant]["is_parent"]
                if is_parent:
                    parents.append(descendant)
                pass

        return parents

    @staticmethod
    def label_related_parents(directed_graph):
        website_rankings = list(directed_graph.nodes)
        for website_ranking in website_rankings:
            directed_graph.nodes[website_ranking]['nearest_parent'] = ParentsDictProxy.find_nearest_parent(directed_graph,
                                                                                          website_ranking)
            directed_graph.nodes[website_ranking]['all_related_parents'] = ParentsDictProxy.find_all_related_parents(directed_graph,
                                                                                                    website_ranking)
            pass

    @staticmethod
    def construct_parents_dictionary(directed_graph):
        parents_dictionary = {}

        website_ranking_ids = list(directed_graph.nodes)
        for website_ranking_id in website_ranking_ids:
            website_ranking_name = directed_graph.nodes[website_ranking_id]['name']

            # this is an expensive operation to be doing a quarter of a mil times
            added_parents = parents_dictionary.keys()

            is_parent = directed_graph.nodes[website_ranking_id]['is_parent']
            is_generic = directed_graph.nodes[website_ranking_id]['is_generic']

            in_dictionary = website_ranking_id in added_parents

            # this will include self
            all_related_parents = directed_graph.nodes[website_ranking_id]['all_related_parents']
            many_parents = len(all_related_parents) > 1

            # decide if to add parents dictionary?
            if is_parent:
                if many_parents:
                    has_parent_in_dictionary = any(
                        [related_parent in added_parents for related_parent in all_related_parents])
                    if not has_parent_in_dictionary and not in_dictionary:
                        parents_dictionary.update(
                            {website_ranking_id: {'org_website_ranking_name': website_ranking_name,
                                                  'generic_cluster': is_generic,
                                                  'related_objects': {website_ranking_id},
                                                  'related_names': {website_ranking_name}}})
                    else:
                        # includes self
                        for related_parent in all_related_parents:
                            related_parent_in_dictionary = related_parent in added_parents
                            if related_parent_in_dictionary:
                                operating_parent = related_parent
                                either_generic = any([directed_graph.nodes[website_ranking_id]['is_generic'],
                                                      parents_dictionary[operating_parent]['generic_cluster']])
                                parents_dictionary[operating_parent]['generic_cluster'] = either_generic
                                break

                elif not in_dictionary:
                    parents_dictionary.update({website_ranking_id: {'org_website_ranking_name': website_ranking_name,
                                                                    'generic_cluster': is_generic,
                                                                    'related_objects': {website_ranking_id},
                                                                    'related_names': {website_ranking_name}}})

                else:
                    either_generic = any([directed_graph.nodes[website_ranking_id]['is_generic'],
                                          parents_dictionary[website_ranking_id]['generic_cluster']])
                    parents_dictionary[website_ranking_id]['generic_cluster'] = either_generic

            else:
                if many_parents:
                    operating_parent = None
                    has_parent_in_dictionary = any(
                        [related_parent in added_parents for related_parent in all_related_parents])
                    if has_parent_in_dictionary:
                        for related_parent in all_related_parents:
                            parent_in_dictionary = related_parent in added_parents
                            if parent_in_dictionary:
                                operating_parent = related_parent
                                either_generic = any([directed_graph.nodes[website_ranking_id]['is_generic'],
                                                      parents_dictionary[operating_parent]['generic_cluster']])
                                parents_dictionary[operating_parent]['generic_cluster'] = either_generic
                                break

                    else:
                        operating_parent = directed_graph.nodes[website_ranking_id]['nearest_parent']

                    if operating_parent is None:
                        operating_parent = directed_graph.nodes[website_ranking_id]['nearest_parent']

                else:
                    operating_parent = directed_graph.nodes[website_ranking_id]['nearest_parent']

                operating_parent_in_dictionary = operating_parent in added_parents
                if operating_parent_in_dictionary:
                    either_generic = any([directed_graph.nodes[website_ranking_id]['is_generic'],
                                          parents_dictionary[operating_parent]['generic_cluster']])
                else:
                    either_generic = any([directed_graph.nodes[website_ranking_id]['is_generic'],
                                          directed_graph.nodes[operating_parent]['is_generic']])
                    operating_parent_name = directed_graph.nodes[operating_parent]['name']
                    parents_dictionary.update({operating_parent: {'org_website_ranking_name': operating_parent_name,
                                                                  'generic_cluster': either_generic,
                                                                  'related_objects': {operating_parent},
                                                                  'related_names': {operating_parent_name}}})

                parents_dictionary[operating_parent]['related_objects'].add(website_ranking_id)
                parents_dictionary[operating_parent]['related_names'].add(website_ranking_name)
                parents_dictionary[operating_parent]['generic_cluster'] = either_generic

        return parents_dictionary
