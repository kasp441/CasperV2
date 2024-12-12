using Domain;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Repo
{
    public class RememberContext : DbContext
    {
        public RememberContext(DbContextOptions<RememberContext> options) : base(options)
        {
        }

        public DbSet<Reminder> Reminders { get; set; }
    }
}
