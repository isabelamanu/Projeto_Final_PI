from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioAdaptado
from django.contrib.auth.models import Group


class UsuarioAdaptadoCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioAdaptado
        fields = [
            'username', 'first_name', 'last_name', 'email', 'cpf', 'nome_cidade', 'nome_mae',  'telefone', 'endereco', 'nome_bairro', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF (apenas números)'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da mãe'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome de usuário' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Senha'}))


class PerfilForm(forms.ModelForm):
    """Formulário para editar perfil do usuário"""
    class Meta:
        model = UsuarioAdaptado
        fields = ['first_name', 'last_name', 'email', 'foto_perfil', 'nome_cidade', 'nome_mae', 'telefone', 'endereco', 'nome_bairro']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da mãe'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'foto_perfil': 'Foto de Perfil',
            'nome_cidade': 'Cidade',
            'nome_mae': 'Nome da Mãe',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
            'nome_bairro': 'Bairro',
        }

class UsuarioFiltroForm(forms.Form):
    """Formulário para filtrar usuários"""
    
    username = forms.CharField(
        required=False, 
        label='Nome de Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por username...'
        })
    )
    
    email = forms.EmailField(
        required=False, 
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por e-mail...'
        })
    )
    
    cidade = forms.CharField(
        required=False, 
        label='Cidade',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por cidade...'
        })
    )
    
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Grupo',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        empty_label="Todos os grupos"
    )
    
    is_active = forms.ChoiceField(
        required=False,
        label='Status',
        choices=[
            ('', 'Todos'),
            ('true', 'Ativo'),
            ('false', 'Inativo')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


class UsuarioEditForm(forms.ModelForm):
    """Formulário para editar usuário (sem senha)"""
    
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Grupos'
    )
    
    class Meta:
        model = UsuarioAdaptado
        fields = [
            'username', 'first_name', 'last_name', 'email', 'cpf', 
            'nome_cidade', 'nome_mae', 'telefone', 'endereco', 'nome_bairro', 
            'foto_perfil', 'is_active', 'is_staff'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_mae': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'cpf': 'CPF',
            'nome_cidade': 'Cidade',
            'nome_mae': 'Nome da Mãe',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
            'nome_bairro': 'Bairro',
            'foto_perfil': 'Foto de Perfil',
            'is_active': 'Usuário Ativo',
            'is_staff': 'Acesso ao Admin',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['grupos'].initial = self.instance.groups.all()
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Atualizar grupos
            if 'grupos' in self.cleaned_data:
                user.groups.set(self.cleaned_data['grupos'])
        return user