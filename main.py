from PartA3_SotiroskiRifat import update_graph
from connection import connect

def main():
    conn = connect()
    print("Connected")
    update_graph(conn)
    print("DONE")

if __name__ == '__main__':
    main()
