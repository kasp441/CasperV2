using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain
{
    public class Reminder
    {
        public int Id { get; set; }
        public string What { get; set; }
        public string Priority { get; set; }
        public string Notes { get; set; }
    }
}
