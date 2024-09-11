##########################################
# - The only demerit of the following
# code is that you need to write the query
# in the folowing order, order is IMP here.

# SELECT
# FROM
# WHERE
# JOIN ON*
##########################################





# TOKENS----------------------------------
(SELECT, FROM, WHERE, JOIN, ON) = ("SELECT", "FROM", "WHERE", "JOIN", "ON")
(UNION, INTERSECT, MINUS) = ("UNION", "INTERSECT", "MINUS")
SET_OPR_SYMBOLS = {
    "UNION": "∪",
    "INTERSECT": "∩",
    "MINUS": "-"
}
# ----------------------------------------

class SQLComponents:
    def __init__(self):
        self.projection_columns = None
        self.table1 = None
        self.selection_cond = None
        self.join_table = None
        self.join_cond = None

    def __str__(self):
        return f"""
        projection_columns = {self.projection_columns}
        table1 = {self.table1}
        selection_cond = {self.selection_cond}
        join_table = {self.join_table}
        join_cond = {self.join_cond}
        """

    def __repr__(self):
        return self.__str__()

class SQLTranslator:
    def __init__(self, query):
        self.query = query

    def translate(self):
        flag = 0
        for OPR in (UNION, INTERSECT, MINUS):
            if OPR in self.query.upper():
                flag = 1
                query1 = self.query[:self.query.upper().find(OPR)].strip()
                operator = OPR
                query2 = self.query[self.query.upper().find(OPR) + len(OPR):].strip()

        if flag:
            final_expression = f"({self.parser(query1)})" + f" {SET_OPR_SYMBOLS.get(operator)} " + f"({self.parser(query2)})"
            return final_expression
        else:
            return self.parser(self.query)

    def lexer(self, query):
        components = SQLComponents()

        # Fill the components attributes
        components.projection_columns = query[query.upper().find(SELECT) + len(SELECT):query.upper().find(FROM):].strip()

        # WHERE Clause
        if WHERE in query.upper():
            # FROM (...) WHERE
            components.table1 = query[query.upper().find(FROM) + len(FROM):query.upper().find(WHERE):].strip()
            if JOIN in query.upper():
                components.selection_cond = query[query.upper().find(WHERE) + len(WHERE):query.upper().find(JOIN):].strip()
                if ON in query.upper():
                    components.join_table = query[query.upper().find(JOIN) + len(JOIN):query.upper().find(ON):].strip()
                    components.join_cond = query[query.upper().find(ON) + len(ON):].strip()
                else:
                    components.join_table = query[query.upper().find(JOIN) + len(JOIN):].strip()
            else:
                components.selection_cond = query[query.upper().find(WHERE) + len(WHERE):].strip()

            components.selection_cond = components.selection_cond.replace(" AND ", " ^ ").replace(" and ", " ^ ").replace(" OR ", " | ").replace(" or ", " | ")
        else:
            components.table1 = query[query.upper().find(FROM) + len(FROM):].strip()

        return components

    def parser(self, query):
        ra_components = self.lexer(query)

        ra_expression = ""

        if ra_components.projection_columns:
            ra_expression += f"π({ra_components.projection_columns})"
        if ra_components.selection_cond:
            ra_expression += f" σ({ra_components.selection_cond})"
        if ra_components.table1:
            ra_expression += f" ({ra_components.table1})"
        if ra_components.join_table:
            if ra_components.join_cond:
                ra_expression += f" ⨝ ({ra_components.join_cond}) ({ra_components.join_table})"
            else:
                ra_expression += f" ⨝ ({ra_components.join_table})"

        return ra_expression

def main():
    while True:
        query = input("Query> ")
        if not query:
            continue

        translator = SQLTranslator(query)
        # breakpoint()
        result = translator.translate()

        print("----------------------------------------------------")
        print(result)
        print("----------------------------------------------------")

if __name__ == '__main__':
    main()