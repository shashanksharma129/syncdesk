// ABOUTME: Students API: GET /me/students for linked students.
import { fetchApi } from "./api";
import type { Student } from "@/lib/types";

export interface StudentApi {
  id: number;
  school_id: number;
  class_name: string;
  section: string;
}

function toStudent(s: StudentApi): Student {
  return {
    id: String(s.id),
    school_id: String(s.school_id),
    name: `Class ${s.class_name}${s.section}`,
    grade: `Grade ${s.class_name}`,
  };
}

export async function fetchStudents(): Promise<Student[]> {
  const list = (await fetchApi<StudentApi[]>("/me/students")) ?? [];
  return list.map(toStudent);
}
