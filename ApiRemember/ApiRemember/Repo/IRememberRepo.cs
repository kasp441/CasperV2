using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Domain;

namespace Repo
{
    public interface IRememberRepo
    {
        //crud for remember
        public void CreateRemember(Reminder reminder);
        public List<Reminder> ReadAllRemember();
        public Reminder ReadRememberById(int id);
        public void UpdateRemember(Reminder reminder);
        public void DeleteRemember(Reminder reminder);
    }
}
