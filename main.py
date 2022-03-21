from PartA3_SotiroskiRifat import update_graph
from PartB_SotiroskiRifat import*
from PartC_SotiroskiRifat import*
from PartD_SotiroskiRifat import*
from connection import connect


def main():
    conn = connect()
    print("Connected")
    update_graph(conn)
    print("DONE")
    #Start of the part B
    #The method will be called from here
    print("Part B query started")
    citation_query(conn)
    communities_query(conn)
    impact_factor_query(conn)
    hindex_query(conn) 
    print("Part B query ended")
    # end of part B
    
    
    #Start of Part C
    print("Part C started")
    louvain(conn)
    shortest_path(conn)
    print("Part C ended")
    #end of part C
    
    
    #start of Part D
    
    print("Part D started")
    step1(conn)
    step2(conn)
    step3(conn)
    step4(conn)
    print("Part D ended")
    
    
    
    #End of part D
    
    
    

if __name__ == '__main__':
    main()
