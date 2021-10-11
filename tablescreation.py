import psycopg2
from config import Config as config
 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
    
        """
        CREATE TABLE IF NOT EXISTS freelancer (
            freelancer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            dateofbirth DATE NOT NULL,
            status VARCHAR(255) NOT NULL,
            skills VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            contact VARCHAR(255) NOT NULL
        )
        """,
        """ 
            CREATE TABLE IF NOT EXISTS employer (
                employer_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                company_description VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                contact VARCHAR(255) NOT NULL
               
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS job_postings (
                job_id SERIAL PRIMARY KEY,
                employer_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL,
                duration VARCHAR(255) NOT NULL,
                no_of_people INTEGER NOT NULL,
                FOREIGN KEY (employer_id)
                  REFERENCES employer (employer_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                amount REAL NOT NULL
                
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS comment (
                comment_id SERIAL PRIMARY KEY,
                employer_id INTEGER NOT NULL,
                freelancer_id INTEGER NOT NULL,
                FOREIGN KEY (employer_id)
                  REFERENCES employer (employer_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (freelancer_id)
                  REFERENCES freelancer (freelancer_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                comment VARCHAR(255) NOT NULL,
                dateofcomment DATE NOT NULL,
                timeofcomment TIME NOT NULL,
                rating INTEGER NOT NULL
                
        )
        """,
        """
            CREATE TABLE IF NOT EXISTS job_allocation (
                freelancer_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                FOREIGN KEY (freelancer_id)
                  REFERENCES freelancer (freelancer_id)
                  ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (job_id)
                  REFERENCES job_postings (job_id)
                  ON UPDATE CASCADE ON DELETE CASCADE
               
                )
        
        """)
    conn = None
    try:
        # read connection parameters
        params = {}
        params['host'] = config.DB_HOSTNAME
        params['password'] = config.DB_PASSWORD
        params['database'] = config.DB_NAME
        params['user'] = config.DB_USERNAME

        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print("Success!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()
