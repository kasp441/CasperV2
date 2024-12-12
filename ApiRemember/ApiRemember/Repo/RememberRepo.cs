using Domain;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Repo
{
    public class RememberRepo : IRememberRepo
    {
        RememberContext _context;
        public RememberRepo(RememberContext context)
        {
            _context = context;
        }
        public void CreateRemember(Reminder reminder)
        {
            _context.Reminders.Add(reminder);
            _context.SaveChanges();
        }

        public void DeleteRemember(Reminder reminder)
        {
            _context.Reminders.Remove(reminder);
            _context.SaveChanges();
        }

        public List<Reminder> ReadAllRemember()
        {
            return _context.Reminders.ToList();
        }

        public Reminder ReadRememberById(int id)
        {
            return _context.Reminders.FirstOrDefault(r => r.Id == id);
        }

        public void UpdateRemember(Reminder reminder)
        {
            _context.Reminders.Update(reminder);
            _context.SaveChanges();
        }
    }
}
