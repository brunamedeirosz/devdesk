import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

function NavLinkItem({ to, children, icon }) {
  const location = useLocation();
  const isActive = location.pathname === to;
  return (
    <Link to={to} className={`nav-link ${isActive ? 'active' : ''}`}>
      <span>{icon}</span>
      {children}
    </Link>
  );
}

function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ workspaces: 0, projetos: 0, tarefas: 0 });

  useEffect(() => {
    Promise.all([
      api.get('workspaces/'),
      api.get('projetos/'),
      api.get('tarefas/')
    ]).then(([ws, proj, task]) => {
      setStats({
        workspaces: ws.data.length,
        projetos: proj.data.length,
        tarefas: task.data.length
      });
    }).catch(err => console.error(err));
  }, []);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Visão geral do sistema</p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/projetos')}>+ Novo Projeto</button>
      </div>

      <div className="grid">
        <div className="card">
          <h3 style={{ marginBottom: '0.5rem', fontSize: '2.5rem', color: 'var(--text-primary)' }}>{stats.workspaces}</h3>
          <h4>Workspaces</h4>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>Ambientes da equipe.</p>
        </div>
        <div className="card">
          <h3 style={{ marginBottom: '0.5rem', fontSize: '2.5rem', color: 'var(--warning)' }}>{stats.projetos}</h3>
          <h4>Projetos Ativos</h4>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>Entregas em andamento.</p>
        </div>
        <div className="card">
          <h3 style={{ marginBottom: '0.5rem', fontSize: '2.5rem', color: 'var(--accent-color)' }}>{stats.tarefas}</h3>
          <h4>Tarefas Totais</h4>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>Ações cadastradas no fluxo.</p>
        </div>
      </div>
    </div>
  );
}

function Workspaces() {
  const [workspaces, setWorkspaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ nome: '', tipo: 'Desenvolvimento' });

  useEffect(() => {
    fetchWorkspaces();
  }, []);

  const fetchWorkspaces = () => {
    api.get('workspaces/').then(res => {
      setWorkspaces(res.data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    api.post('workspaces/', formData).then(res => {
      setWorkspaces([...workspaces, res.data]);
      setShowForm(false);
      setFormData({ nome: '', tipo: 'Desenvolvimento' });
    });
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Workspaces</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Organização de áreas e clientes</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Criar Workspace'}
        </button>
      </div>
      
      {showForm && (
        <form className="card" onSubmit={handleSubmit} style={{marginBottom: '2rem', maxWidth: '500px'}}>
          <h3 style={{marginBottom: '1.5rem'}}>Novo Workspace</h3>
          <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
            <input required type="text" placeholder="Nome do Workspace" className="form-input"
              value={formData.nome} onChange={e => setFormData({...formData, nome: e.target.value})} />
            
            <select required className="form-input" value={formData.tipo} 
              onChange={e => setFormData({...formData, tipo: e.target.value})}>
              <option value="Desenvolvimento">Desenvolvimento</option>
              <option value="Marketing">Marketing</option>
              <option value="Design">Design</option>
              <option value="Gestão">Gestão</option>
            </select>
            
            <button type="submit" className="btn btn-primary" style={{alignSelf: 'flex-start'}}>Salvar</button>
          </div>
        </form>
      )}

      {loading ? (
        <p style={{ color: 'var(--text-muted)' }}>Carregando dados da API...</p>
      ) : (
        <div className="grid">
          {workspaces.length === 0 && !showForm ? (
            <p style={{ color: 'var(--text-muted)' }}>Nenhum workspace encontrado no banco de dados.</p>
          ) : (
            workspaces.map(ws => (
              <div key={ws.id} className="card">
                <h3 style={{ marginBottom: '0.5rem' }}>{ws.nome}</h3>
                <span style={{ 
                  backgroundColor: 'var(--bg-surface-hover)', color: 'var(--text-secondary)',
                  padding: '0.25rem 0.75rem', borderRadius: '20px', fontSize: '0.8rem'
                }}>
                  {ws.tipo}
                </span>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

function Projetos() {
  const [projetos, setProjetos] = useState([]);
  const [workspaces, setWorkspaces] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nome: '', descricao: '', status: 'Em Planejamento', prazo_entrega: '', workspace: ''
  });

  useEffect(() => {
    api.get('projetos/').then(res => setProjetos(res.data));
    api.get('workspaces/').then(res => setWorkspaces(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    api.post('projetos/', formData)
      .then(res => {
        setProjetos([...projetos, res.data]);
        setShowForm(false);
        setFormData({nome: '', descricao: '', status: 'Em Planejamento', prazo_entrega: '', workspace: ''});
      }).catch(err => console.error(err));
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Projetos</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Gerencie os projetos ativos.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Novo Projeto'}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleSubmit} style={{marginBottom: '2rem'}}>
          <h3 style={{marginBottom: '1.5rem'}}>Criar Novo Projeto</h3>
          <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
            <input required type="text" placeholder="Nome do Projeto" className="form-input"
              value={formData.nome} onChange={e => setFormData({...formData, nome: e.target.value})} />
            
            <textarea required placeholder="Descrição" rows="3" className="form-input"
              value={formData.descricao} onChange={e => setFormData({...formData, descricao: e.target.value})} />
            
            <select required className="form-input" value={formData.workspace} 
              onChange={e => setFormData({...formData, workspace: e.target.value})}>
              <option value="">Selecione o Workspace</option>
              {workspaces.map(ws => <option key={ws.id} value={ws.id}>{ws.nome}</option>)}
            </select>

            <select required className="form-input" value={formData.status} 
              onChange={e => setFormData({...formData, status: e.target.value})}>
              <option value="Em Planejamento">Em Planejamento</option>
              <option value="Em Andamento">Em Andamento</option>
              <option value="Concluído">Concluído</option>
            </select>
            
            <input required type="datetime-local" className="form-input"
              value={formData.prazo_entrega} onChange={e => setFormData({...formData, prazo_entrega: e.target.value})} />
            
            <button type="submit" className="btn btn-primary" style={{alignSelf: 'flex-start', marginTop: '0.5rem'}}>
              Salvar Projeto
            </button>
          </div>
        </form>
      )}

      <div className="grid">
        {projetos.length === 0 && !showForm ? (
           <p style={{ color: 'var(--text-muted)' }}>Nenhum projeto encontrado.</p>
        ) : (
          projetos.map(proj => (
            <div key={proj.id} className="card">
              <h3 style={{ marginBottom: '0.5rem' }}>{proj.nome}</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
                {proj.descricao}
              </p>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ 
                    backgroundColor: proj.status === 'Concluído' ? 'var(--success)' : 'var(--bg-surface-hover)', 
                    color: proj.status === 'Concluído' ? 'white' : 'var(--text-secondary)',
                    padding: '0.25rem 0.75rem', borderRadius: '20px', fontSize: '0.8rem'
                  }}>
                  {proj.status}
                </span>
                <span style={{color: 'var(--text-muted)', fontSize: '0.8rem'}}>
                  Prazo: {new Date(proj.prazo_entrega).toLocaleDateString('pt-BR')}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function Tarefas() {
  const [tarefas, setTarefas] = useState([]);
  const [projetos, setProjetos] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    titulo: '', descricao: '', prioridade: 'Média', status: 'A Fazer', prazo_entrega: '', projeto: ''
  });

  useEffect(() => {
    api.get('tarefas/').then(res => setTarefas(res.data));
    api.get('projetos/').then(res => setProjetos(res.data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    api.post('tarefas/', formData).then(res => {
      setTarefas([...tarefas, res.data]);
      setShowForm(false);
      setFormData({titulo: '', descricao: '', prioridade: 'Média', status: 'A Fazer', prazo_entrega: '', projeto: ''});
    }).catch(err => console.error(err));
  };

  const aFazer = tarefas.filter(t => t.status === 'A Fazer');
  const fazendo = tarefas.filter(t => t.status === 'Em Andamento');
  const feito = tarefas.filter(t => t.status === 'Concluído');

  const renderColumn = (title, items, colorVar) => (
    <div style={{ flex: 1, minWidth: '300px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <h3 style={{ borderBottom: `2px solid var(${colorVar})`, paddingBottom: '0.5rem', color: 'var(--text-primary)' }}>
        {title} ({items.length})
      </h3>
      {items.map(t => (
        <div key={t.id} className="card" style={{ padding: '1rem', borderLeft: `4px solid var(${colorVar})` }}>
          <h4 style={{ marginBottom: '0.5rem' }}>{t.titulo}</h4>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1rem' }}>{t.descricao}</p>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
              Prioridade: <span style={{color: t.prioridade === 'Alta' ? 'var(--danger)' : 'var(--accent-color)'}}>{t.prioridade}</span>
            </span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {new Date(t.prazo_entrega).toLocaleDateString('pt-BR')}
            </span>
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Tarefas</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Acompanhamento de demandas diárias via Kanban.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nova Tarefa'}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleSubmit} style={{marginBottom: '2rem'}}>
          <h3 style={{marginBottom: '1.5rem'}}>Cadastrar Tarefa</h3>
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
            <input required type="text" placeholder="Título da Tarefa" className="form-input" style={{gridColumn: '1 / -1'}}
              value={formData.titulo} onChange={e => setFormData({...formData, titulo: e.target.value})} />
            
            <textarea required placeholder="Descrição detalhada" rows="2" className="form-input" style={{gridColumn: '1 / -1'}}
              value={formData.descricao} onChange={e => setFormData({...formData, descricao: e.target.value})} />
            
            <select required className="form-input" value={formData.projeto} 
              onChange={e => setFormData({...formData, projeto: e.target.value})}>
              <option value="">Projeto Relacionado</option>
              {projetos.map(p => <option key={p.id} value={p.id}>{p.nome}</option>)}
            </select>

            <select required className="form-input" value={formData.prioridade} 
              onChange={e => setFormData({...formData, prioridade: e.target.value})}>
              <option value="Baixa">Prioridade: Baixa</option>
              <option value="Média">Prioridade: Média</option>
              <option value="Alta">Prioridade: Alta</option>
            </select>

            <select required className="form-input" value={formData.status} 
              onChange={e => setFormData({...formData, status: e.target.value})}>
              <option value="A Fazer">A Fazer</option>
              <option value="Em Andamento">Em Andamento</option>
              <option value="Concluído">Concluído</option>
            </select>
            
            <input required type="datetime-local" className="form-input"
              value={formData.prazo_entrega} onChange={e => setFormData({...formData, prazo_entrega: e.target.value})} />
            
            <button type="submit" className="btn btn-primary" style={{gridColumn: '1 / -1', justifySelf: 'start', marginTop: '0.5rem'}}>
              Salvar Tarefa
            </button>
          </div>
        </form>
      )}

      {/* KANBAN BOARD */}
      <div style={{ display: 'flex', gap: '1.5rem', overflowX: 'auto', paddingBottom: '1rem' }}>
        {renderColumn("A Fazer", aFazer, "--border-color")}
        {renderColumn("Em Andamento", fazendo, "--warning")}
        {renderColumn("Concluído", feito, "--success")}
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <aside className="sidebar">
          <div className="sidebar-logo">
            <span style={{ color: 'var(--accent-color)' }}>✦</span> DevDesk
          </div>
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <NavLinkItem to="/" icon="🏠">Dashboard</NavLinkItem>
            <NavLinkItem to="/workspaces" icon="📁">Workspaces</NavLinkItem>
            <NavLinkItem to="/projetos" icon="📋">Projetos</NavLinkItem>
            <NavLinkItem to="/tarefas" icon="✅">Tarefas</NavLinkItem>
          </nav>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/workspaces" element={<Workspaces />} />
            <Route path="/projetos" element={<Projetos />} />
            <Route path="/tarefas" element={<Tarefas />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
