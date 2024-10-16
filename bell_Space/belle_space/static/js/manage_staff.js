function addStaff(appointment_id, csrf_token){
    const stf = document.getElementById('input-add-staff');
        const staff_id = stf.value;W
        
        // กำหนด path ให้ถูกต้อง
        fetch(`/appointment/${appointment_id}/${staff_id}/add/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
            }
        })
        .then(response => response.json())
        .then(data => { 
            console.log('Item updated successfully')
            window.location.reload()
        })
        .catch(error => console.error('Error:', error));
}

