document.addEventListener("DOMContentLoaded",() => {
  async function get_subjects() {
    subject?.replaceChildren(optionUndefined)
    // @ts-ignore
    const params = new URLSearchParams();
    // @ts-ignore
    params.append("grade_id",grade.value)

    const response = await fetch(`/panel/api/get/?${params}`);

    const jsonResponse = await response.json();
    
    if (!jsonResponse.subjects) {
      return
    }

    jsonResponse.subjects.forEach(element => {
      const option = new Option(element[1],element[0])
      subject?.appendChild(option)
    });
  }
  
  const grade = document.querySelector("#grade");
  const subject = document.querySelector("#subject");
  // @ts-ignore
  const optionUndefined = new Option("---------","");
  grade?.addEventListener("change",get_subjects)

});