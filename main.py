from PartA3_SotiroskiRifat import update_graph
from PartB_SotiroskiRifat import run_all_queries
from PartC_SotiroskiRifat import run_algorithms
from PartD_SotiroskiRifat import run_recommender
from connection import connect


def main():
    conn = connect()
    print("Connected")

    # Part A
    update_graph(conn)
    print("Graph Updated")

    #Start of the part B
    print("Part B query started")
    run_all_queries(conn)
    print("Part B query ended")
    # end of part B

    #Start of Part C
    print("Part C started")
    run_algorithms(conn)
    print("Part C ended")
    #end of part C
    
    
    #start of Part D
    print("Part D started")
    run_recommender(conn)
    print("Part D ended")
    #End of part D
    
    
    

if __name__ == '__main__':
    main()
