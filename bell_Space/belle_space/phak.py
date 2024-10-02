class AppointmentForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    staff_id = forms.ModelChoiceField(
        queryset=Staff.objects.all(),
        required=True
    )
    class Meta:
        model = Appointment
        fields = ['staff_id', 
                'category',
                'services', 
                'appointment_date',

                ]
        labels = {
            'staff_id': 'พนักงาน',
            'category': 'หมวดหมู่',
            'services': 'บริการ',
            'appointment_date': 'วันที่นัดหมาย',

        }
        widgets = {
            'staff_id': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'appointment_date': DateInput(attrs={
                'type': 'date',
                'class': 'p-2 rounded-md'
            }),
            
            'category': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            
        }

    def clean(self):
        cleaned_data = super().clean()
        app_date = cleaned_data.get('appointment_date')
        now = timezone.now()

        if app_date and app_date < now:
            raise ValidationError("จองย้อนไม่ได้จ้า")
        
        return cleaned_data
