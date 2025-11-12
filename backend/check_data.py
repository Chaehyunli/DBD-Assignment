"""
Database data verification script
Checks if all data has been properly inserted
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def check_data():
    """Check data in all tables"""
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        print("=" * 80)
        print("DATABASE DATA VERIFICATION")
        print("=" * 80)
        print()

        # Tables to check with expected counts
        tables_to_check = [
            ("department", 3, "dept_code, dept_name"),
            ("course", 6, "course_code, course_name, credits"),
            ("professor", 5, "professor_id, professor_name, dept_code"),
            ("student", 10, "student_id, student_name, grade_year, dept_code"),
            ("lecture", 12, "lecture_id, semester, course_code, professor_id"),
            ("enrollment", 60, "student_id, lecture_id, grade"),
            ("student_semester_gpa", 20, "student_id, semester, semester_gpa, earned_credits")
        ]

        all_passed = True

        for table_name, expected_count, columns in tables_to_check:
            # Get count
            cur.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            result = cur.fetchone()
            actual_count = result['count']

            status = "✓" if actual_count == expected_count else "✗"

            if actual_count != expected_count:
                all_passed = False

            print(f"{status} {table_name.upper()}")
            print(f"   Expected: {expected_count} records, Actual: {actual_count} records")

            # Show sample data (first 3 records)
            cur.execute(f"SELECT {columns} FROM {table_name} LIMIT 3")
            samples = cur.fetchall()

            if samples:
                print(f"   Sample data:")
                for i, sample in enumerate(samples, 1):
                    print(f"      {i}. {dict(sample)}")

            print()

        # Additional checks
        print("=" * 80)
        print("ADDITIONAL VERIFICATION")
        print("=" * 80)
        print()

        # Check if lecture IDs are auto-generated
        cur.execute("SELECT lecture_id FROM lecture ORDER BY lecture_id")
        lecture_ids = [row['lecture_id'] for row in cur.fetchall()]
        print(f"✓ Lecture IDs (auto-generated): {lecture_ids}")
        print()

        # Check foreign key relationships
        cur.execute("""
            SELECT s.student_name, d.dept_name
            FROM student s
            JOIN department d ON s.dept_code = d.dept_code
            LIMIT 3
        """)
        print("✓ Student-Department relationship (sample):")
        for row in cur.fetchall():
            print(f"   - {row['student_name']} → {row['dept_name']}")
        print()

        # Check enrollment with student and lecture info
        cur.execute("""
            SELECT s.student_name, c.course_name, e.grade
            FROM enrollment e
            JOIN student s ON e.student_id = s.student_id
            JOIN lecture l ON e.lecture_id = l.lecture_id
            JOIN course c ON l.course_code = c.course_code
            LIMIT 5
        """)
        print("✓ Enrollment data (sample):")
        for row in cur.fetchall():
            print(f"   - {row['student_name']} enrolled in {row['course_name']} (Grade: {row['grade']})")
        print()

        # Summary
        print("=" * 80)
        if all_passed:
            print("✓ ALL DATA VERIFICATION PASSED!")
        else:
            print("✗ SOME TABLES HAVE INCORRECT RECORD COUNTS")
        print("=" * 80)

        # Close connection
        cur.close()
        conn.close()

        return all_passed

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_data()
    exit(0 if success else 1)
